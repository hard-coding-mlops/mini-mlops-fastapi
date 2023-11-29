import torch
from tqdm import tqdm, tqdm_notebook
from transformers.optimization import get_cosine_schedule_with_warmup

class Trainer():
    def __init__(self, model, optimizer, loss_fn, device):
        self.model = model
        self.optimizer = optimizer
        self.loss_fn = loss_fn
        self.device = device
        super().__init__()

    #정확도 측정을 위한 함수 정의
    def _calc_accuracy(self, X, Y):
        max_vals, max_indices = torch.max(X, 1)
        train_acc = (max_indices == Y).sum().data.cpu().numpy()/max_indices.size()[0]
        return train_acc

    def _train(self, train_dataloader, config, scheduler ,e):
        train_acc = 0.0

        self.model.train()
        # token_ids: 토큰의 인덱스
        # valid_length: 실제 데이터의 길이
        # segment_ids: 세그먼트 ID (일부 모델에서 사용)
        for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(tqdm_notebook(train_dataloader)):
            self.optimizer.zero_grad()
            token_ids = token_ids.long().to(self.device)
            segment_ids = segment_ids.long().to(self.device) 
            valid_length= valid_length
            label = label.long().to(self.device)
            out = self.model(token_ids, valid_length, segment_ids)
            
            loss = self.loss_fn(out, label)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), config.max_grad_norm)
            self.optimizer.step()
            scheduler.step()  # Update learning rate schedule
            train_acc += self.calc_accuracy(out, label)
            if batch_id % config.log_interval == 0:
                print("epoch {} batch id {} loss {} train acc {}".format(e+1, batch_id+1, loss.data.cpu().numpy(), train_acc / (batch_id+1)))
        print("epoch {} train acc {}".format(e+1, train_acc / (batch_id+1)))
        return train_acc

    def _validate(self, test_dataloader, config, e):
        test_acc = 0.0
        self.model.eval()
        for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(tqdm_notebook(test_dataloader)):
            token_ids = token_ids.long().to(self.device)
            segment_ids = segment_ids.long().to(self.device)
            valid_length= valid_length
            label = label.long().to(self.device)
            out = self.model(token_ids, valid_length, segment_ids)
            test_acc += self._calc_accuracy(out, label)
        print("epoch {} test acc {}".format(e+1, test_acc / (batch_id+1)))
        return test_acc

    def train(self, train_dataloader, test_dataloader, config):
        print("train Start")
        t_total = len(train_dataloader) * config.num_epochs
        warmup_step = int(t_total * config.warmup_ratio)

        scheduler = get_cosine_schedule_with_warmup(self.optimizer, num_warmup_steps=warmup_step, num_training_steps=t_total)

        for e in range(config.num_epochs):
            train_acc = self._train(train_dataloader,config, scheduler, e)
            test_acc = self._validate(test_dataloader,config, e)
        print("train End")
        #########################################################################################

        # Restore to best model.
        # self.model.load_state_dict(best_model)