
import logging, uuid
# import agent import trace,
def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | trace_id=%(trace_id)s | %(message)s"
    )

def generate_trace_id():
    return str(uuid.uuid4())[:8]

def get_logger(trace_id):
    logger = logging.getLogger(__name__)
    def log(level, msg):
        logger.log(getattr(logging, level), msg, extra={"trace_id": trace_id})
    return log
