"""
WitFoo Custom pySigma Processing Pipelines

Defines field mapping and transformation pipelines for converting WitFoo Sigma
rules to platform-specific query languages. Since the artifact-exporter sends
identical camelCase JSON fields to all platforms, the pipelines are minimal.

Platform notes:
  - Splunk: HEC wraps artifact JSON in {"event": "<json>"}, extract via spath
  - OpenSearch: Direct JSON indexing — fields are 1:1
  - Sentinel: wrappedArtifact promotes fields to top-level + TimeGenerated
"""

from sigma.processing.conditions import LogsourceCondition
from sigma.processing.pipeline import ProcessingItem, ProcessingPipeline
from sigma.processing.transformations import (
    FieldMappingTransformation,
    ChangeLogsourceTransformation,
)


def witfoo_splunk_pipeline() -> ProcessingPipeline:
    """
    Pipeline for Splunk SPL output.

    The artifact-exporter writes HEC events with the artifact JSON as a string
    inside the `event` field. After `| spath`, all camelCase fields become
    available as Splunk fields. No field name transformation needed.
    """
    return ProcessingPipeline(
        name="WitFoo Splunk Pipeline",
        priority=20,
        items=[
            ProcessingItem(
                identifier="witfoo_splunk_logsource",
                transformation=ChangeLogsourceTransformation(
                    product="witfoo",
                    service="artifact-exporter",
                ),
                rule_conditions=[
                    LogsourceCondition(product="witfoo"),
                ],
            ),
        ],
    )


def witfoo_opensearch_pipeline() -> ProcessingPipeline:
    """
    Pipeline for OpenSearch DQL/Lucene output.

    The artifact-exporter indexes artifact JSON directly (artifact mode).
    All fields are 1:1 with the Sigma rule field names. Minimal transformation.
    """
    return ProcessingPipeline(
        name="WitFoo OpenSearch Pipeline",
        priority=20,
        items=[
            ProcessingItem(
                identifier="witfoo_opensearch_logsource",
                transformation=ChangeLogsourceTransformation(
                    product="witfoo",
                    service="artifact-exporter",
                ),
                rule_conditions=[
                    LogsourceCondition(product="witfoo"),
                ],
            ),
        ],
    )


def witfoo_sentinel_pipeline() -> ProcessingPipeline:
    """
    Pipeline for Microsoft Sentinel KQL output.

    The artifact-exporter sends artifacts via Data Collection Rules (DCR) to
    a custom table (WitFoo_CL). The wrappedArtifact struct promotes artifact
    fields to top level + adds TimeGenerated. Field names map 1:1 except
    for the _CL suffix convention on the table name.
    """
    return ProcessingPipeline(
        name="WitFoo Sentinel Pipeline",
        priority=20,
        items=[
            ProcessingItem(
                identifier="witfoo_sentinel_logsource",
                transformation=ChangeLogsourceTransformation(
                    product="witfoo",
                    service="artifact-exporter",
                ),
                rule_conditions=[
                    LogsourceCondition(product="witfoo"),
                ],
            ),
        ],
    )
