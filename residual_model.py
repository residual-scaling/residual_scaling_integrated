import threading
import time
from util import load_model, load_db


class ResidualModel:
    def __init__(self, model, model_type: str = "local", db_type: str = "vector"):
        self.model_type = model_type
        self.model = load_model(model_type, model)
        self.db = load_db(db_type)
        self.distillation_queue = []
        self.lock = threading.Lock()
        threading.Thread.__init__(self, target=self.process_distillation_queue)

    def process_distillation_queue(self):
        while True:
            time.sleep(3)
            print("[Distill] check distillation queue")
            while len(self.distillation_queue) > 0:
                cur_context = self.distillation_queue.pop(0)
                self.lock.acquire()
                print(f"[Distill] distilling 1 out of {len(self.distillation_queue) + 1}")
                distilled_context = self.model.generate_distillation(cur_context)
                self.db.put(distilled_context)
                self.lock.release()
                # sleep 0.1s to give user query processing the priority, creating a pseudo priority lock
                time.sleep(0.1)
            print("[Distill] distillation queue clean!")

    def query(self, query: str) -> str:
        self.lock.acquire()
        print("--- Start query() --- ")
        self.model.generate_answer(query)
        print("--- Finish query() --- ")
        self.lock.release()
        return

    def query_with_residual(self, query: str) -> str:
        self.lock.acquire()
        print("--- Start query_with_residual() --- ")
        related_contexts = self.db.get(query)
        context = ",".join(related_contexts)
        result = self.model.generate_answer(query, context)
        self.distillation_queue.append(f"Query: {query}; Result:{result}")
        print("--- Finish query_with_residual() --- ")
        self.lock.release()
        return result
