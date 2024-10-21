from typing import Any

class CheckConfigFollower:
    
    @staticmethod
    def checkConfigPartner(
        configFollower: Any,
        configData: str,
        configOperation: str,
    ):
        result = "" 

        for config in configFollower.config:
            if config.data == configData:
                if len(config.operations) > 0 :
                    for operations in config.operations:
                        if operations == configOperation:
                            result = operations        
                else:
                    result = 0

        return result