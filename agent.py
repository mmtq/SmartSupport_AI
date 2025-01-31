from langchain_groq import ChatGroq
from langchain.schema import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
class AICustomerSupportAgent:
    def __init__(self):
        self.llm = ChatGroq(model="llama-3.2-3b-preview")
        
    def interpret_and_evaluate(self, extracted_properties):
        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an AI Customer Support Agent. Respond politely and helpfully. Provide one reply only."),
            ("human", 
             "Check out the extracted properties from the email: {extracted_properties} , The customer's email is categorized as given category and mentions the product as mentioned_product. "
             "Issue description: as issue_description. "
             "Write a friendly and helpful response, addressing the problem and offering a solution. "
             "Address the user by name if provided in the email, otherwise say 'Dear Customer'. "
             "Sign off as Mir Tarhimul.")
        ])
        chain = chat_prompt | self.llm | StrOutputParser()
        response = chain.invoke({"extracted_properties": extracted_properties})
        return response

        
    def extract_properties(self, email_body):
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an AI that extracts structured information from emails."),
            ("human",f"Extract the following information from this email:\n- Category (complaint, refund_request, product_feedback, customer_service, other)\n- Mentioned product\n- Issue description (brief summary)\n- Name of sender\n\nEmail Content:\n{email_body}")
        ])
        chain = prompt | self.llm | StrOutputParser()
        extracted_properties = chain.invoke({"email_body": email_body})
        return extracted_properties
    
    def process_email(self, email_data):
        extracted_properties = self.extract_properties(email_data["body"])        
        evaluation_result = self.interpret_and_evaluate(extracted_properties)
        print(evaluation_result)
        return evaluation_result

if __name__ == "__main__":
    agent = AICustomerSupportAgent()
    email_data = {
        "sender_name": "John Doe",
        "sender_addr": "mirsalmanfarsi@gmail.com",
        "subject": "My Phone is Not Working",
        "body": "hi, the samsung a30 phone that I bought from your store is not working properly. I would like to request a refund. Thanks. from, bob",
    }
    agent.process_email(email_data)