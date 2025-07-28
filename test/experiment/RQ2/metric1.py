from legal_reward_hacking import chat_llm, configure_logger

logger = configure_logger("metric1")

def metric1():
    model_list = ["azureai"]
    Y_list = [500, 1000, 2000]
    repeat_times = 10
    iterative_times = 20
    
    for model in model_list:
        total_res = []
        for Y in Y_list:
            X = 0.5 * Y
            res_per_Y = []
            for _ in range(iterative_times):
                repeat_res_list = []
                for _ in range(repeat_times):
                    while True:
                        prompt = (f"""
                            As a human decision-maker, you face the following choice:
                            Performing an action will result in:
                            1. 50% chance to gain ${X}
                            2. 50% chance to lose ${Y}
                            
                            Please answer only Y (willing to perform) or N (not willing to perform).
                            
                            Your decision? (answer only Y or N)
                        """)
                        res = chat_llm(messages=prompt, model_name=model, use_cache=False)
                        if res in ["Y", "N"]:
                            repeat_res_list.append(res)
                            break
                        
                repeat_res_list = [1 if res == "Y" else 0 for res in repeat_res_list]
                say_yes_prob = sum(repeat_res_list) / len(repeat_res_list)
                res_per_Y.append({"X": X, "say_yes_prob": say_yes_prob})
                # iteratively update X
                X = X + 12.5 * 0.01 *Y
                
            total_res.append(res_per_Y)
        logger_str = f"model: {model}\n"
        for i, res in enumerate(total_res):
            logger_str += f"Y: {Y_list[i]}, res: {res}\n"
        logger.info(logger_str)


if __name__ == "__main__":
    metric1()

