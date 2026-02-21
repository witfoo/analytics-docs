.PHONY: all splunk opensearch sentinel validate test clean

CONVERTER_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
SIGMA_DIR := $(CONVERTER_DIR)../../docs/detection-rules/sigma
OUTPUT_BASE := $(CONVERTER_DIR)../../docs/detection-rules

all: splunk opensearch sentinel

splunk:
	cd $(CONVERTER_DIR) && python convert.py --target splunk --output $(OUTPUT_BASE)/splunk/

opensearch:
	cd $(CONVERTER_DIR) && python convert.py --target opensearch --output $(OUTPUT_BASE)/opensearch/

sentinel:
	cd $(CONVERTER_DIR) && python convert.py --target sentinel --output $(OUTPUT_BASE)/sentinel/

validate:
	cd $(CONVERTER_DIR) && python convert.py --target all --validate-only

test:
	cd $(CONVERTER_DIR) && pytest test_rules.py test_convert.py -v

test-rules:
	cd $(CONVERTER_DIR) && pytest test_rules.py -v

test-convert:
	cd $(CONVERTER_DIR) && pytest test_convert.py -v

clean:
	rm -rf $(OUTPUT_BASE)/splunk/rules/
	rm -rf $(OUTPUT_BASE)/opensearch/rules/
	rm -rf $(OUTPUT_BASE)/sentinel/rules/
	rm -f $(OUTPUT_BASE)/splunk/all_rules.spl
	rm -f $(OUTPUT_BASE)/opensearch/all_rules.dql
	rm -f $(OUTPUT_BASE)/sentinel/all_rules.kql
