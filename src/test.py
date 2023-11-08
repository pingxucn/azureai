import os 
# from dotenv import load_dotenv

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

def main(): 
        
    try: 
    
        # Get configuration settings 
        # load_dotenv()
        form_endpoint = os.getenv('AZURE_FORM_RECOGNIZER_ENDPOINT')
        form_key = os.getenv('AZURE_FORM_RECOGNIZER_KEY')
        
        # Create client using endpoint and key
        document_analysis_client = DocumentAnalysisClient(
            endpoint=form_endpoint, credential=AzureKeyCredential(form_key)
        )

        # Model ID from when you trained your model.
        model_id = os.getenv('AZURE_FORM_RECOGNIZER_MODEL_ID')

        # Test trained model with a new form 
        ## from azure storage
        file_url = "https://rstorage2speech.blob.core.windows.net/speechtest/2310.11511.pdf?sp=r&st=2023-11-08T00:25:47Z&se=2023-11-08T08:25:47Z&spr=https&sv=2022-11-02&sr=b&sig=0gIGt042dSVHPbezQZOj4D%2FD9XGS8qt5s5u3vk4DkOc%3D"
        poller = document_analysis_client.begin_analyze_document_from_url(model_id=model_id, document_url=file_url)

        ## from local file
        # file_path = "../data/pdf/test/2308.00479.pdf"
        # with open(file_path, "rb") as f: 
        #     poller = document_analysis_client.begin_analyze_document(model_id=model_id, document=f)

        result = poller.result()
        
        for idx, document in enumerate(result.documents):
            print("--------Analyzing document #{}--------".format(idx + 1))
            print("Document has type {}".format(document.doc_type))
            print("Document has confidence {}".format(document.confidence))
            print("Document was analyzed by model with ID {}".format(result.model_id))
            for name, field in document.fields.items():
                field_value = field.value if field.value else field.content
                print("......found field of type '{}' with value '{}' and with confidence {}".format(field.value_type, field_value, field.confidence))


        # iterate over tables, lines, and selection marks on each page
        print(f"Total number of pages: {len(result.pages)}")
        # for page in result.pages:
        #     print("\nLines found on page {}".format(page.page_number))
        #     for line in page.lines:
        #         print("...Line '{}'".format(line.content.encode('utf-8')))
        #     for word in page.words:
        #         print(
        #             "...Word '{}' has a confidence of {}".format(
        #                 word.content.encode('utf-8'), word.confidence
        #             )
        #         )
        #     for selection_mark in page.selection_marks:
        #         print(
        #             "...Selection mark is '{}' and has a confidence of {}".format(
        #                 selection_mark.state, selection_mark.confidence
        #             )
        #         )

        # for i, table in enumerate(result.tables):
        #     print("\nTable {} can be found on page:".format(i + 1))
        #     for region in table.bounding_regions:
        #         print("...{}".format(i + 1, region.page_number))
        #     for cell in table.cells:
        #         print(
        #             "...Cell[{}][{}] has content '{}'".format(
        #                 cell.row_index, cell.column_index, cell.content.encode('utf-8')
        #             )
        #         )
        print("-----------------------------------")
        
    except Exception as ex:
        print(ex)

if __name__ == '__main__': 
    main()