"""
Dashboard validation tests for WitFoo SIEM Analytics platform dashboards.

Tests structural validity of:
- Splunk SimpleXML dashboards
- OpenSearch NDJSON dashboard exports
- Microsoft Sentinel ARM template workbooks
- Sentinel analytics rules ARM template
"""

import json
import os
import xml.etree.ElementTree as ET

import pytest
import yaml

BASE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'docs', 'detection-rules')

# ============================================================================
# Splunk Dashboard Tests
# ============================================================================

SPLUNK_APP_DIR = os.path.join(BASE_DIR, 'splunk', 'witfoo_siem_app')

EXPECTED_SPLUNK_DASHBOARDS = [
    'witfoo_network_overview.xml',
    'witfoo_security_alerts.xml',
    'witfoo_attack_coverage.xml',
    'witfoo_top_talkers.xml',
    'witfoo_protocol_analysis.xml',
]


class TestSplunkApp:
    """Test Splunk app structure and configuration."""

    def test_app_conf_exists(self):
        assert os.path.exists(os.path.join(SPLUNK_APP_DIR, 'default', 'app.conf'))

    def test_app_conf_has_required_stanzas(self):
        conf_path = os.path.join(SPLUNK_APP_DIR, 'default', 'app.conf')
        with open(conf_path) as f:
            content = f.read()
        assert '[launcher]' in content
        assert '[ui]' in content
        assert '[install]' in content
        assert 'WitFoo' in content

    def test_metadata_exists(self):
        assert os.path.exists(os.path.join(SPLUNK_APP_DIR, 'metadata', 'default.meta'))

    def test_savedsearches_exists(self):
        assert os.path.exists(os.path.join(SPLUNK_APP_DIR, 'default', 'savedsearches.conf'))

    def test_savedsearches_has_rules(self):
        conf_path = os.path.join(SPLUNK_APP_DIR, 'default', 'savedsearches.conf')
        with open(conf_path) as f:
            content = f.read()
        # Count stanzas (each starts with [WitFoo - )
        stanza_count = content.count('[WitFoo - ')
        assert stanza_count == 55, f"Expected 55 saved searches, got {stanza_count}"


class TestSplunkDashboards:
    """Test Splunk SimpleXML dashboard validity."""

    @pytest.fixture(params=EXPECTED_SPLUNK_DASHBOARDS)
    def dashboard_path(self, request):
        return os.path.join(SPLUNK_APP_DIR, 'default', 'data', 'ui', 'views', request.param)

    def test_all_dashboards_exist(self):
        views_dir = os.path.join(SPLUNK_APP_DIR, 'default', 'data', 'ui', 'views')
        for name in EXPECTED_SPLUNK_DASHBOARDS:
            assert os.path.exists(os.path.join(views_dir, name)), f"Missing dashboard: {name}"

    def test_valid_xml(self, dashboard_path):
        """Each dashboard must be valid XML."""
        tree = ET.parse(dashboard_path)
        root = tree.getroot()
        assert root.tag in ('dashboard', 'form'), f"Root tag should be 'dashboard' or 'form', got '{root.tag}'"

    def test_has_label(self, dashboard_path):
        """Each dashboard must have a label."""
        tree = ET.parse(dashboard_path)
        root = tree.getroot()
        label = root.find('label')
        assert label is not None and label.text, "Dashboard must have a non-empty <label>"

    def test_has_panels(self, dashboard_path):
        """Each dashboard must have at least one panel."""
        tree = ET.parse(dashboard_path)
        root = tree.getroot()
        panels = root.findall('.//panel')
        assert len(panels) >= 1, "Dashboard must have at least one panel"

    def test_panels_have_searches(self, dashboard_path):
        """Each panel must have a search query."""
        tree = ET.parse(dashboard_path)
        root = tree.getroot()
        for panel in root.findall('.//panel'):
            # Panels contain chart/table/single/map elements with search children
            search_elements = panel.findall('.//search')
            assert len(search_elements) >= 1, f"Panel must have at least one <search> element"

    def test_queries_reference_witfoo_index(self, dashboard_path):
        """All SPL queries should reference the witfoo index."""
        tree = ET.parse(dashboard_path)
        root = tree.getroot()
        for query in root.findall('.//query'):
            if query.text:
                assert 'index=witfoo' in query.text, f"Query should reference witfoo index: {query.text[:80]}"


# ============================================================================
# OpenSearch Dashboard Tests
# ============================================================================

OPENSEARCH_DIR = os.path.join(BASE_DIR, 'opensearch')

EXPECTED_OPENSEARCH_DASHBOARDS = [
    'witfoo_network_overview.ndjson',
    'witfoo_security_alerts.ndjson',
    'witfoo_attack_coverage.ndjson',
    'witfoo_top_talkers.ndjson',
    'witfoo_protocol_analysis.ndjson',
]


class TestOpenSearchIndexTemplate:
    """Test OpenSearch index template."""

    def test_index_template_exists(self):
        assert os.path.exists(os.path.join(OPENSEARCH_DIR, 'index_template.json'))

    def test_index_template_valid_json(self):
        with open(os.path.join(OPENSEARCH_DIR, 'index_template.json')) as f:
            template = json.load(f)
        assert 'index_patterns' in template
        assert 'witfoo-*' in template['index_patterns']

    def test_index_template_has_mappings(self):
        with open(os.path.join(OPENSEARCH_DIR, 'index_template.json')) as f:
            template = json.load(f)
        # Index template v2 nests under template.mappings
        mappings = template.get('mappings', template.get('template', {}).get('mappings', {}))
        assert mappings, "Template must have mappings"
        props = mappings['properties']
        # Check key fields are mapped
        assert 'clientIP' in props
        assert 'serverIP' in props
        assert 'startTimeUTC' in props
        assert 'totalBytes' in props


class TestOpenSearchDashboards:
    """Test OpenSearch NDJSON dashboard exports."""

    @pytest.fixture(params=EXPECTED_OPENSEARCH_DASHBOARDS)
    def dashboard_path(self, request):
        return os.path.join(OPENSEARCH_DIR, 'dashboards', request.param)

    def test_all_dashboards_exist(self):
        dashboards_dir = os.path.join(OPENSEARCH_DIR, 'dashboards')
        for name in EXPECTED_OPENSEARCH_DASHBOARDS:
            assert os.path.exists(os.path.join(dashboards_dir, name)), f"Missing dashboard: {name}"

    def test_valid_ndjson(self, dashboard_path):
        """Each line must be valid JSON."""
        with open(dashboard_path) as f:
            lines = f.readlines()
        assert len(lines) >= 2, "NDJSON file must have at least 2 objects (index-pattern + dashboard)"
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                pytest.fail(f"Line {i+1} is not valid JSON: {e}")
            assert 'id' in obj, f"Line {i+1} missing 'id'"
            assert 'type' in obj, f"Line {i+1} missing 'type'"

    def test_has_index_pattern(self, dashboard_path):
        """Each NDJSON must include an index-pattern object."""
        with open(dashboard_path) as f:
            lines = f.readlines()
        types = []
        for line in lines:
            line = line.strip()
            if line:
                obj = json.loads(line)
                types.append(obj.get('type'))
        assert 'index-pattern' in types, "Must include an index-pattern saved object"

    def test_has_dashboard_object(self, dashboard_path):
        """Each NDJSON must include a dashboard object."""
        with open(dashboard_path) as f:
            lines = f.readlines()
        types = []
        for line in lines:
            line = line.strip()
            if line:
                obj = json.loads(line)
                types.append(obj.get('type'))
        assert 'dashboard' in types, "Must include a dashboard saved object"

    def test_has_visualizations(self, dashboard_path):
        """Each NDJSON must include visualization objects."""
        with open(dashboard_path) as f:
            lines = f.readlines()
        viz_count = 0
        for line in lines:
            line = line.strip()
            if line:
                obj = json.loads(line)
                if obj.get('type') == 'visualization':
                    viz_count += 1
        assert viz_count >= 3, f"Expected at least 3 visualizations, got {viz_count}"

    def test_index_pattern_references_witfoo(self, dashboard_path):
        """Index pattern should use witfoo-* pattern."""
        with open(dashboard_path) as f:
            lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line:
                obj = json.loads(line)
                if obj.get('type') == 'index-pattern':
                    title = obj.get('attributes', {}).get('title', '')
                    assert 'witfoo' in title.lower(), f"Index pattern should reference witfoo: {title}"


# ============================================================================
# Sentinel Workbook Tests
# ============================================================================

SENTINEL_DIR = os.path.join(BASE_DIR, 'sentinel')

EXPECTED_SENTINEL_WORKBOOKS = [
    'witfoo_network_overview.json',
    'witfoo_security_alerts.json',
    'witfoo_attack_coverage.json',
]


class TestSentinelWorkbooks:
    """Test Microsoft Sentinel ARM template workbooks."""

    @pytest.fixture(params=EXPECTED_SENTINEL_WORKBOOKS)
    def workbook_path(self, request):
        return os.path.join(SENTINEL_DIR, 'workbooks', request.param)

    def test_all_workbooks_exist(self):
        workbooks_dir = os.path.join(SENTINEL_DIR, 'workbooks')
        for name in EXPECTED_SENTINEL_WORKBOOKS:
            assert os.path.exists(os.path.join(workbooks_dir, name)), f"Missing workbook: {name}"

    def test_valid_json(self, workbook_path):
        """Each workbook must be valid JSON."""
        with open(workbook_path) as f:
            template = json.load(f)
        assert isinstance(template, dict)

    def test_arm_template_structure(self, workbook_path):
        """Must follow ARM template structure."""
        with open(workbook_path) as f:
            template = json.load(f)
        assert '$schema' in template, "Missing $schema"
        assert 'resources' in template, "Missing resources"
        assert 'parameters' in template, "Missing parameters"
        assert len(template['resources']) >= 1, "Must have at least one resource"

    def test_workbook_resource_type(self, workbook_path):
        """Resource type must be Microsoft.Insights/workbooks."""
        with open(workbook_path) as f:
            template = json.load(f)
        for resource in template['resources']:
            assert resource['type'] == 'Microsoft.Insights/workbooks'

    def test_has_workspace_parameter(self, workbook_path):
        """Must accept workspaceResourceId parameter."""
        with open(workbook_path) as f:
            template = json.load(f)
        assert 'workspaceResourceId' in template['parameters']


class TestSentinelAnalyticsRules:
    """Test Sentinel analytics rules ARM template."""

    @pytest.fixture
    def rules_template(self):
        path = os.path.join(SENTINEL_DIR, 'analytics_rules.json')
        with open(path) as f:
            return json.load(f)

    def test_analytics_rules_exists(self):
        assert os.path.exists(os.path.join(SENTINEL_DIR, 'analytics_rules.json'))

    def test_valid_arm_template(self, rules_template):
        assert '$schema' in rules_template
        assert 'resources' in rules_template

    def test_has_55_rules(self, rules_template):
        assert len(rules_template['resources']) == 55, \
            f"Expected 55 analytics rules, got {len(rules_template['resources'])}"

    def test_all_rules_are_scheduled(self, rules_template):
        for resource in rules_template['resources']:
            assert resource['kind'] == 'Scheduled'

    def test_all_rules_disabled_by_default(self, rules_template):
        for resource in rules_template['resources']:
            assert resource['properties']['enabled'] is False

    def test_all_rules_have_queries(self, rules_template):
        for resource in rules_template['resources']:
            query = resource['properties']['query']
            assert len(query) > 10, "Query must be non-trivial"

    def test_all_rules_have_severity(self, rules_template):
        valid_severities = {'High', 'Medium', 'Low', 'Informational'}
        for resource in rules_template['resources']:
            sev = resource['properties']['severity']
            assert sev in valid_severities, f"Invalid severity: {sev}"

    def test_rules_have_witfoo_prefix(self, rules_template):
        for resource in rules_template['resources']:
            name = resource['properties']['displayName']
            assert name.startswith('WitFoo: '), f"Rule should have WitFoo prefix: {name}"


# ============================================================================
# Cross-Platform Consistency Tests
# ============================================================================

class TestCrossPlatformConsistency:
    """Test that all platforms have consistent coverage."""

    def test_splunk_rules_count(self):
        rules_dir = os.path.join(BASE_DIR, 'splunk', 'rules')
        spl_files = [f for f in os.listdir(rules_dir) if f.endswith('.spl') and f != 'all_rules.spl']
        assert len(spl_files) == 55, f"Expected 55 Splunk rules, got {len(spl_files)}"

    def test_opensearch_rules_count(self):
        rules_dir = os.path.join(BASE_DIR, 'opensearch', 'rules')
        dql_files = [f for f in os.listdir(rules_dir) if f.endswith('.dql') and f != 'all_rules.dql']
        assert len(dql_files) == 55, f"Expected 55 OpenSearch rules, got {len(dql_files)}"

    def test_sentinel_rules_count(self):
        rules_dir = os.path.join(BASE_DIR, 'sentinel', 'rules')
        kql_files = [f for f in os.listdir(rules_dir) if f.endswith('.kql') and f != 'all_rules.kql']
        assert len(kql_files) == 55, f"Expected 55 Sentinel rules, got {len(kql_files)}"

    def test_all_platforms_same_count(self):
        splunk_count = len([f for f in os.listdir(os.path.join(BASE_DIR, 'splunk', 'rules'))
                          if f.endswith('.spl') and f != 'all_rules.spl'])
        opensearch_count = len([f for f in os.listdir(os.path.join(BASE_DIR, 'opensearch', 'rules'))
                               if f.endswith('.dql') and f != 'all_rules.dql'])
        sentinel_count = len([f for f in os.listdir(os.path.join(BASE_DIR, 'sentinel', 'rules'))
                             if f.endswith('.kql') and f != 'all_rules.kql'])
        assert splunk_count == opensearch_count == sentinel_count, \
            f"Platform rule counts differ: Splunk={splunk_count}, OpenSearch={opensearch_count}, Sentinel={sentinel_count}"

    def test_dashboard_count_consistency(self):
        """All platforms should have 5 dashboards."""
        splunk_views = os.path.join(SPLUNK_APP_DIR, 'default', 'data', 'ui', 'views')
        splunk_count = len([f for f in os.listdir(splunk_views) if f.endswith('.xml')])

        os_dashboards = os.path.join(OPENSEARCH_DIR, 'dashboards')
        os_count = len([f for f in os.listdir(os_dashboards) if f.endswith('.ndjson')])

        sentinel_workbooks = os.path.join(SENTINEL_DIR, 'workbooks')
        # Sentinel has 3 workbooks (network, security, attack) - fewer than others per plan
        sentinel_count = len([f for f in os.listdir(sentinel_workbooks) if f.endswith('.json')])

        assert splunk_count == 5, f"Expected 5 Splunk dashboards, got {splunk_count}"
        assert os_count == 5, f"Expected 5 OpenSearch dashboards, got {os_count}"
        assert sentinel_count == 3, f"Expected 3 Sentinel workbooks, got {sentinel_count}"
