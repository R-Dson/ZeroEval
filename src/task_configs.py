from datasets import load_dataset
from _TEMPLATES import apply_mc_template, apply_lgp_grid_template

def mapping_task_names(data_name):
    id_name = "id"
    if data_name == "mmlu-redux":
        dataset = load_dataset("yuchenlin/zero-eval", "mmlu-redux", split="test")
    elif data_name == "gsm":
        dataset = load_dataset("yuchenlin/zero-eval", "gsm", split="test")
    elif data_name == "zebra-grid":
        dataset = load_dataset("allenai/ZebraLogicBench", "grid_mode", split="test")
    elif data_name == "alpaca_eval":
        dataset = load_dataset("tatsu-lab/alpaca_eval", "alpaca_eval", split="eval")  
    else:
        raise ValueError(f"Data name {data_name} not supported")
    return dataset, id_name

def prompt_generation(data_name, data_item, args):
    if data_name in ["mmlu-redux"]:  # and other multiple-choice QA dataset 
        prompt = apply_mc_template(data_item, cot = args.cot) 
    elif data_name in ["alpaca_eval"]:
        prompt = data_item["instruction"]
    elif data_name in ["zebra-grid"]:
        prompt = apply_lgp_grid_template(data_item, cot = args.cot) 
    else:
        raise ValueError(f"Data name {data_name} not supported")
    return prompt

def result_format(output_item, args):
    if args.data_name in ["alpaca_eval"]:
        output_item["output"] = output_item["output"][0] # use str instead of list 
    return output_item