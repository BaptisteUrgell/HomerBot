from readline import replace_history_item
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch 

MODEL = "DingleyMaillotUrgell/homer-bot"
# MODEL = "microsoft/DialoGPT-small"

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL)

# Let's chat for 5 lines
for step in range(5):
    # encode the new user input, add the eos_token and return a tensor in Pytorch
    new_user_input_ids = tokenizer.encode(input(">> User: ") + tokenizer.eos_token, return_tensors='pt')
    # print(new_user_input_ids)

    # append the new user input tokens to the chat history
    bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

    # generated a response while limiting the total chat history to 1000 tokens, 
    chat_history_ids = model.generate(
        bot_input_ids, 
        max_length=1000,                    
        pad_token_id=tokenizer.eos_token_id,  
        no_repeat_ngram_size=3,
        # # num_beams = 50       
        do_sample=True, 
        top_k=100, 
        top_p=0.7,
        # length_penalty = 0.5,
        temperature = 0.8
        # repetition_penalty=1.3 
    )
    
    # pretty print last ouput tokens from bot
    print("Homer: {}".format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))
