from __future__ import annotations

from dataclasses import dataclass

from pydantic_graph import BaseNode, End, Graph, GraphRunContext

from mergemind.agents.repairer import run_repair_agent
from mergemind.agents.reviewer import run_review_agent
from mergemind.models.domain import ReviewReport
from mergemind.models.review_packet import ReviewPacket
from mergemind.models.state import ReviewState
from mergemind.retrieval.mock_packet_builder import MockPacketBuilder


@dataclass
class BuildPrNode(BaseNode[ReviewState, None, ReviewReport]):
    async def run(self, ctx: GraphRunContext[ReviewState, None]) -> ResolvePbiNode:
        builder = MockPacketBuilder()
        ctx.state.pr = builder.build_pr(ctx.state.request)
        return ResolvePbiNode()


@dataclass
class ResolvePbiNode(BaseNode[ReviewState, None, ReviewReport]):
    async def run(self, ctx: GraphRunContext[ReviewState, None]) -> RetrieveContextNode:
        builder = MockPacketBuilder()
        ctx.state.pbi = builder.build_pbi(ctx.state.request)
        return RetrieveContextNode()


@dataclass
class RetrieveContextNode(BaseNode[ReviewState, None, ReviewReport]):
    async def run(self, ctx: GraphRunContext[ReviewState, None]) -> AssemblePacketNode:
        builder = MockPacketBuilder()
        ctx.state.retrieved_chunks = builder.build_retrieved_chunks()
        return AssemblePacketNode()


@dataclass
class AssemblePacketNode(BaseNode[ReviewState, None, ReviewReport]):
    async def run(self, ctx: GraphRunContext[ReviewState, None]) -> RunReviewNode:
        if ctx.state.pr is None:
            ctx.state.errors.append("Pull request not built")
            raise ValueError("Pull request not built")

        ctx.state.packet = ReviewPacket(
            pr=ctx.state.pr,
            pbi=ctx.state.pbi,
            retrieved_chunks=ctx.state.retrieved_chunks,
        )
        return RunReviewNode()


@dataclass
class RunReviewNode(BaseNode[ReviewState, None, ReviewReport]):
    async def run(self, ctx: GraphRunContext[ReviewState, None]) -> ValidateReportNode:
        if ctx.state.packet is None:
            ctx.state.errors.append("ReviewPacket not assembled")
            raise ValueError("ReviewPacket not assembled")

        ctx.state.report = await run_review_agent(ctx.state.packet)
        return ValidateReportNode()


@dataclass
class ValidateReportNode(BaseNode[ReviewState, None, ReviewReport]):
    async def run(
        self, ctx: GraphRunContext[ReviewState, None]
    ) -> RepairReportNode | End[ReviewReport]:
        if ctx.state.report is None:
            ctx.state.errors.append("Review report not generated")
            raise ValueError("Review report not generated")

        report = ctx.state.report
        ctx.state.warnings.clear()

        if report.missing_acceptance_criteria and report.alignment_score >= 1.0:
            ctx.state.warnings.append(
                "alignment_score is 1.0 despite missing acceptance criteria"
            )

        if not report.missing_acceptance_criteria and report.alignment_score < 0.5:
            ctx.state.warnings.append(
                "alignment_score seems low despite no missing acceptance criteria"
            )

        if report.confidence > 0.95 and (
            ctx.state.pbi is None or not ctx.state.retrieved_chunks
        ):
            ctx.state.warnings.append(
                "confidence is very high despite limited supporting evidence"
            )

        if ctx.state.warnings and ctx.state.repair_attempts < 1:
            return RepairReportNode()

        return End(report)


@dataclass
class RepairReportNode(BaseNode[ReviewState, None, ReviewReport]):
    async def run(self, ctx: GraphRunContext[ReviewState, None]) -> ValidateReportNode:
        if ctx.state.report is None:
            ctx.state.errors.append("No review report available for repair")
            raise ValueError("No review report available for repair")

        ctx.state.report = await run_repair_agent(
            ctx.state.report,
            ctx.state.warnings,
        )
        ctx.state.repair_attempts += 1

        return ValidateReportNode()


review_graph = Graph[ReviewState, None, ReviewReport](
    nodes=(
        BuildPrNode,
        ResolvePbiNode,
        RetrieveContextNode,
        AssemblePacketNode,
        RunReviewNode,
        ValidateReportNode,
        RepairReportNode,
    ),
)
