from argparse import ArgumentParser
import logging
import sys
from core.deployer import SalesforceDeployer

def main():
    parser = ArgumentParser(description="Salesforce Schema Deployment Tool")
    
    parser.add_argument('--config', type=str, required=True, help='Path to the JSON configuration file')
    parser.add_argument('--env', type=str, default='.env', help='Path to the .env file with credentials')
    parser.add_argument('--output', type=str, default=None, help='Path to store deployment files')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    parser.add_argument('--no-deploy', action='store_true', help='Generate metadata files without deploying')
    parser.add_argument('--validate', action='store_true', help='Validate the JSON structure without deployment')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting deployment process...")
        deployer = SalesforceDeployer(args.config, args.output, args.env)
        
        if args.validate:
            logger.info("Validation completed successfully.")
            return
        
        deployer.generate_metadata()
        
        if not args.no_deploy:
            deployer.deploy_metadata()
        
        deployer.summarize_deployment()
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()