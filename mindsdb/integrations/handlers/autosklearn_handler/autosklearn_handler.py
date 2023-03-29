from typing import Optional, Dict

import dill
import pandas as pd
import autosklearn.classification as automl
from autosklearn.metrics import accuracy

from mindsdb.integrations.libs.base import BaseMLEngine


class AutoSklearnHandler(BaseMLEngine):
    """
    Integration with the Auto-Sklearn ML library.
    """

    name = 'autosklearn'

    def create(self, target: str, df: Optional[pd.DataFrame] = None, args: Optional[dict] = None) -> None:
        automl_classifier = automl.AutoSklearnClassifier(
            time_left_for_this_task=600,
            per_run_time_limit=360,
            n_jobs=-1,
            metric=accuracy
        )

        automl_classifier.fit(df.drop(target, axis=1), df[target])

        best_model = automl_classifier.get_models_with_weights()[0][0]

        self.model_storage.file_set('model', dill.dumps(best_model))
        self.model_storage.json_set('args', args)

    def predict(self, df: Optional[pd.DataFrame] = None, args: Optional[dict] = None) -> None:
        model = dill.loads(self.model_storage.file_get('model'))

        return model.predict(df)