import asyncio
from src.geval_framework.llm_as_a_judge import Evaluator

def geval():
    evaluator = Evaluator()
    
    # Run evaluation synchronously
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        response = loop.run_until_complete(evaluator.run())
        return response
    finally:
        loop.close()