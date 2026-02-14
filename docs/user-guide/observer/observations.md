# Observations

Observations are freeform notes and findings recorded during security investigations. They capture analyst insights, external research, and contextual information that complements the structured data in work units and MO definitions.

## Observation Properties

| Field | Description |
| --- | --- |
| **Title** | Brief summary of the observation |
| **Content** | Detailed findings (supports markdown) |
| **Author** | Analyst who recorded the observation |
| **Related incident** | Associated incident (optional) |
| **Related work unit** | Associated work unit (optional) |
| **Tags** | Freeform labels for categorization |
| **Timestamp** | When the observation was recorded |

## Creating Observations

1. Navigate to **Observer** > **Observations**
2. Click **Create Observation**
3. Enter a title and detailed content
4. Optionally link to an incident or work unit
5. Add relevant tags
6. Click **Save**

Observations can also be created from the incident detail page or work unit detail page for quick contextual notes.

## Use Cases

- **Investigation notes** — Document findings during incident analysis
- **External intelligence** — Record relevant information from external sources
- **Analyst handoff** — Leave context for the next shift or team member
- **Lessons learned** — Post-incident notes for future reference
- **Evidence documentation** — Capture screenshots, logs, or analysis results

## Search and Filter

Search observations by:

- Text content (full-text search)
- Author
- Tags
- Date range
- Associated incident or work unit

## Relationship to Other Observer Components

Observations complement the structured data in the Observer module:

- **Work units** track what was done and how long it took
- **Work collections** group related work
- **MO definitions** describe known patterns
- **Observations** capture everything else — the human context that makes investigations meaningful
