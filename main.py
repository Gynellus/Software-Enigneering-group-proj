# Import necessary functions
from convert import convert_input_to_string
from summarize import summarize
from find_similar_papers import find_similar_papers

def main(input_data):
    print("start")
    # Step 1: Read the input paper
    paper_text = convert_input_to_string(input_data)

    print("Step 1 done")
    # Step 2: Summarize the input paper
    input_paper_summary = summarize(paper_text)
    print("Summary of the input paper:")
    print(input_paper_summary)

    print("Step 2 done")
    # Step 3: Find similar papers
    similar_papers = find_similar_papers(paper_text)
    print(similar_papers)

    print("Step 3 done")
    # Step 4: Summarize each similar paper
    similar_paper_summaries = []
    for paper in similar_papers:
        paper_url = paper.split("URL: ")[1].split(",")[0]
        paper_text = convert_input_to_string(paper_url)
        paper_summary = summarize(paper_text)
        similar_paper_summaries.append((paper, paper_summary))

    print("Step 4 done")
    # Print summaries of similar papers
    for idx, (paper_info, summary) in enumerate(similar_paper_summaries):
        print(f"\nSimilar Paper {idx+1}:")
        print(paper_info)
        print("Summary:")
        print(summary)

# Example usage
input_data = "https://arxiv.org/pdf/1805.02343.pdf"  # URL or a local PDF file or a string
main(input_data)