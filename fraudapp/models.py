from django.db import models

class FraudDetectionModel(models.Model):
    is_fraud = models.BooleanField()
    predicted_probability = models.FloatField()

    def __str__(self):
        return f'Fraud: {self.is_fraud} | Probability: {self.predicted_probability}'
