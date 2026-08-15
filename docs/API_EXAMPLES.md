# API Usage Examples

This document provides simple examples for interacting with the resume evaluation backend.

## Health check

Use the deployed backend URL to confirm that the service is available before sending a resume for evaluation.

## Resume evaluation workflow

The application workflow is:

1. Upload a resume PDF through the frontend or API client.
2. Provide the target job description.
3. Extract and clean resume text.
4. Calculate TF-IDF cosine similarity.
5. Compare explicit technical skills.
6. Return semantic similarity, skill match, and the weighted final score.

## Example response shape

```json
{
  "final_score": 75.87,
  "semantic_similarity": 65.53,
  "skill_match": 100.0,
  "matched_skills": ["python", "aws", "docker"],
  "missing_skills": []
}
```

Field names may vary with future API revisions. The README should be treated as the high-level architecture reference, while this file can be expanded with endpoint-specific examples as the API evolves.

## Testing suggestions

Try job descriptions with different levels of overlap and compare:

- High textual and skill overlap
- Similar responsibilities but different terminology
- Strong skill overlap with weak overall text similarity
- Missing technical skills

These cases are useful for understanding how the weighted score behaves.
