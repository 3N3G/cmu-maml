
from data import MetaLearningSystemDataLoader
from experiment_builder import ExperimentBuilder
from few_shot_learning_system import MAMLFewShotClassifier
from utils.parser_utils import get_args
from utils.dataset_tools import maybe_unzip_dataset
from logger_utils import setup_logger, trace_calls  # Add this import

# Setup logger
logger = setup_logger()

@trace_calls
def main():
    try:
        # Log start of experiment setup
        logger.info("Starting MAML experiment setup")
        
        # Get arguments
        logger.debug("Parsing arguments")
        args, device = get_args()
        logger.info(f"Using device: {device}")
        logger.debug(f"Parsed arguments: {vars(args)}")
        
        # Initialize model
        logger.info("Initializing MAML model")
        model = MAMLFewShotClassifier(
            args=args, 
            device=device,
            im_shape=(2, args.image_channels, args.image_height, args.image_width)
        )
        logger.debug(f"Model architecture initialized with shape: {(2, args.image_channels, args.image_height, args.image_width)}")
        
        # Handle dataset
        logger.info("Preparing dataset")
        maybe_unzip_dataset(args=args)
        
        # Setup data loader
        logger.info("Initializing data loader")
        data = MetaLearningSystemDataLoader
        
        # Build experiment
        logger.info("Building experiment")
        maml_system = ExperimentBuilder(model=model, data=data, args=args, device=device)
        
        # Run experiment
        logger.info("Starting experiment")
        maml_system.run_experiment()
        
    except Exception as e:
        logger.error(f"Fatal error in experiment: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
