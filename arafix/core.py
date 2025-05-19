from .model import AraFixModel
from .preprocess import preprocess
from .postprocess import postprocess

class AraFix:
    def __init__(self):
        self.model = AraFixModel()
        
    def correct(self, text):
        """Full pipeline: preprocess -> model -> postprocess"""
        
        # correct multiple sentences
        if isinstance(text, list):
            preprocessed = [preprocess(t) for t in text]
            print("Correcting ...")
            model_outputs = [self.model.predict(t)[0] for t in preprocessed if t]
            postprocessed = [postprocess(t) for t in model_outputs]
            return postprocessed

        # correct a single sentence
        preprocessed = preprocess(text)
        print("Correcting ...")
        model_output = self.model.predict(preprocessed)
        model_output = model_output[0]
        postprocessed = postprocess(model_output)
        return postprocessed
    
    
    def evaluate(self, references, hypotheses):

        from jiwer import cer, wer
        from .der import der

        refs = [references] if isinstance(references, str) else references
        hyps = [hypotheses] if isinstance(hypotheses, str) else hypotheses
        
        cer_score = cer(refs, hyps)
        wer_score = wer(refs, hyps)
        
        der_scores = [der(ref, hyp) for ref, hyp in zip(refs, hyps)]
        der_score = sum(der_scores) / len(der_scores) if der_scores else 0

        metrics = {
            "cer": cer(references, hypotheses),
            "wer": wer(references, hypotheses),
            "der": sum(der_scores) / len(der_scores) if der_scores else 0,
        }

        return metrics
