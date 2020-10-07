import config
import torch

class BERTDataset:
    def __init__(self, review, target):
        self.review = review
        self.target = target
        self.tokenizer = config.TOKENIZER
        self.max_len = config.MAX_LEN
    
    def __len__(self):
        return len(self.review)
    
    def __getitem__(self, item):
        review = str(self.review)
        review = " ".join(review.split())
        inputs = self.tokenizer.encode_plus(
            review,
            None,
            add_special_tokens = True,
            max_length = self.max_len
        )
        ids = inputs["input_ids"]
        mask = inputs["attention_mask"]
        token_type_ids = inputs["token_type_ids"]
        padding_length = self.max_len - len(ids)
        ids = ids + ([0] * padding_length)
        mask = mask + ([0] * padding_length)
        token_type_ids = token_type_ids + ([0] * padding_length)

        return {
            'ids':torch.Tensor(ids, dtype = torch.long),
            'mask':torch.Tensor(mask, dtype = torch.long),
            'token_type_ids':torch.Tensor(token_type_ids, dtype = torch.long),
            'target':torch.Tensor(self.target[item], dtype = torch.float)
        }