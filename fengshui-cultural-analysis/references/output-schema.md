# Output schema

The following is a minimum shape, not a replacement for domain-specific provenance.

{
  "not_prediction": true,
  "analysis_context": {
    "extent": "user supplied extent",
    "orientation": {"north_bearing_degrees": 0},
    "scale": "declared radius or resolution"
  },
  "data_quality": {
    "status": "pass|degraded|hold",
    "checks": [],
    "layer_records": [],
    "degraded_metrics": [],
    "hold_reason": null
  },
  "spatial_metrics": {
    "elevation": {
      "value": {},
      "units": "m",
      "source": "source identifier",
      "method": "tool and algorithm",
      "coverage": 1.0,
      "missing": null
    }
  },
  "cultural_interpretation": [
    {
      "concept": "闈犲北",
      "evidence_metric_ids": ["elevation.rear_sector"],
      "reading": "conditional cultural reading",
      "boundary": "non-causal boundary"
    }
  ],
  "heuristic_cultural_index": {
    "value": 0.0,
    "scale": [0.0, 1.0],
    "components": {},
    "weights": {},
    "coverage": 1.0,
    "meaning": "heuristic cultural summary, not prediction"
  },
  "sensitivity": {
    "method": "one-at-a-time weight perturbation",
    "scenarios": [],
    "range": [0.0, 0.0],
    "stability": "stable|conditional|unstable"
  },
  "uncertainty": [],
  "limitations": []
}

Required top-level fields are data_quality, spatial_metrics, cultural_interpretation, heuristic_cultural_index, sensitivity, uncertainty, and limitations. Preserve not_prediction: true even when the analysis is degraded.

