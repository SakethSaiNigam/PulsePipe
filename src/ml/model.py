from dataclasses import dataclass
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

@dataclass
class ChurnModelSpec:
    C: float = 1.0
    max_iter: int = 1000

def build_model(spec: ChurnModelSpec | None = None) -> Pipeline:
    spec = spec or ChurnModelSpec()
    clf = Pipeline(steps=[
        ("scaler", StandardScaler()),
        ("logreg", LogisticRegression(C=spec.C, max_iter=spec.max_iter))
    ])
    return clf
