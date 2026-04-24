from Agents import search_agent , reader_agent , writer_chain , critical_thinking_chain


def run_research_pipeline(topic: str) -> dict:

    state = {}
    # Step 1: Search Agent search  for information
    print(f"Running Search Agent for topic: {topic}")
    search_results = search_agent().invoke(
        {
            "messages": [("user" , f"Search for recent and reliable information on the topic: {topic}")]
        }
    )
    state["search_results"] = search_results['messages'][-1].content
    print(f"Search Agent completed. Found information:\n{state['search_results']}\n")



    # Step 2: Reader Agent - Read and extract insights from URLs
    print(f"Running Reader Agent to extract insights from search results.")
    scraped_contents = reader_agent().invoke(
        {
           "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}"
        )]
           })
                       
    state["scraped_content"] = scraped_contents['messages'][-1].content
    print(f"Reader Agent completed. Extracted content:\n{state['scraped_content']}\n")




    # Step 3: Writer_Chain - Write the research report

    research_combined = f"Search Results:\n{state['search_results']}\n\nScraped Content:\n{state['scraped_content']}"
    research_report = writer_chain.invoke({
        "topic": topic,
        "research":research_combined
    })
    
    state["research_report"] = research_report
    print(f"Writer Chain completed. Generated research report:\n{state['research_report']}\n")


    # Step 4: Critical Thinking Chain  - Apply critical thinking to evaluate the report
    feedback = critical_thinking_chain.invoke({
         "report" : state['research_report']
          } )
       
    state["critical_feedback"] = feedback

    print(f"Critical Thinking Chain completed. Feedback on the report:\n{state['critical_feedback']}\n")

    return state 


if __name__ == "__main__":
    topic = input("/n Enter a research topic: ")
    run_research_pipeline(topic)


    