def sample_abstractive_summarization(document) -> None:
    # [START abstract_summary]
    import os
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import TextAnalyticsClient

    endpoint = os.environ["AZURE_LANGUAGE_ENDPOINT"]
    key = os.environ["AZURE_LANGUAGE_KEY"]

    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

    poller = text_analytics_client.begin_abstract_summary(document)
    abstract_summary_results = poller.result()
    for result in abstract_summary_results:
        if result.kind == "AbstractiveSummarization":
            print("Summaries abstracted:")
            [print(f"{summary.text}\n") for summary in result.summaries]
        elif result.is_error is True:
            print("...Is an error with code '{}' and message '{}'".format(
                result.error.code, result.error.message
            ))
    # [END abstract_summary]


if __name__ == "__main__":
    audio_file_path = "C:\\Repository\\azure\\azureai\\data\\speech\\yearwiththesaints_00_anonymous.txt" 
    with open(audio_file_path, 'r') as file:
        lines = [line.strip('\n') for line in file.readlines()]
    separator = ', '
    result = [separator.join(lines)]
    sample_abstractive_summarization(result)