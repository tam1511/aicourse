"""
RAG Evaluation for Korea Study Consultant Chatbot.

This module evaluates both retrieval quality and answer quality.
"""

import math
from pydantic import BaseModel, Field
from typing import List, Tuple
from test_questions import TestQuestion, load_tests_from_jsonl


class RetrievalMetrics(BaseModel):
    """Metrics for evaluating retrieval quality."""
    mrr: float = Field(description="Mean Reciprocal Rank - how quickly we find relevant docs")
    ndcg: float = Field(description="Normalized DCG - quality of ranking")
    keyword_coverage: float = Field(description="Percentage of keywords found in top-K")
    keywords_found: int = Field(description="Number of keywords actually found")
    total_keywords: int = Field(description="Total keywords expected")


class AnswerMetrics(BaseModel):
    """Metrics for evaluating answer quality."""
    accuracy: float = Field(description="Factual correctness (1-5)")
    completeness: float = Field(description="Coverage of all needed info (1-5)")
    relevance: float = Field(description="Direct answer to question (1-5)")
    feedback: str = Field(description="Detailed evaluation feedback")


# ============================================
# RETRIEVAL EVALUATION
# ============================================

def calculate_mrr(keyword: str, retrieved_chunks: List) -> float:
    """
    Calculate Mean Reciprocal Rank for a single keyword.
    
    MRR = 1 / rank_of_first_relevant_doc
    If keyword appears in 1st doc: MRR = 1.0
    If keyword appears in 3rd doc: MRR = 0.333
    If keyword not found: MRR = 0.0
    
    Args:
        keyword: The keyword to search for
        retrieved_chunks: List of retrieved document chunks
        
    Returns:
        MRR score (0.0 to 1.0)
    """
    keyword_lower = keyword.lower()
    
    for rank, chunk in enumerate(retrieved_chunks, start=1):
        # Check if keyword appears in the chunk's content
        if keyword_lower in chunk.page_content.lower():
            return 1.0 / rank
    
    return 0.0  # Keyword not found


def calculate_dcg(relevances: List[int], k: int) -> float:
    """
    Calculate Discounted Cumulative Gain.
    
    DCG rewards relevant docs appearing early in results.
    Formula: DCG = Σ (relevance_i / log2(i + 1))
    
    Args:
        relevances: List of relevance scores (1 or 0 for binary)
        k: Number of positions to consider
        
    Returns:
        DCG score
    """
    dcg = 0.0
    for i in range(min(k, len(relevances))):
        # i+2 because: rank starts at 1, and log2(1) = 0
        dcg += relevances[i] / math.log2(i + 2)
    return dcg


def calculate_ndcg(keyword: str, retrieved_chunks: List, k: int = 10) -> float:
    """
    Calculate Normalized Discounted Cumulative Gain.
    
    nDCG normalizes DCG by comparing to ideal ranking.
    Score of 1.0 = perfect ranking
    Score of 0.0 = keyword not found
    
    Args:
        keyword: The keyword to search for
        retrieved_chunks: List of retrieved chunks
        k: Number of top chunks to consider
        
    Returns:
        nDCG score (0.0 to 1.0)
    """
    keyword_lower = keyword.lower()
    
    # Binary relevance: 1 if keyword found, 0 otherwise
    relevances = []
    for chunk in retrieved_chunks[:k]:
        if keyword_lower in chunk.page_content.lower():
            relevances.append(1)
        else:
            relevances.append(0)
    
    # Calculate DCG with actual ranking
    dcg = calculate_dcg(relevances, k)
    
    # Calculate ideal DCG (best case: all relevant docs at top)
    ideal_relevances = sorted(relevances, reverse=True)
    idcg = calculate_dcg(ideal_relevances, k)
    
    # Normalize
    if idcg > 0:
        return dcg / idcg
    else:
        return 0.0


def evaluate_retrieval(
    question: str,
    expected_keywords: List[str],
    retriever,
    k: int = 10
) -> Tuple[RetrievalMetrics, List]:
    """
    Evaluate retrieval performance for a single question.
    
    Args:
        question: The user's question
        expected_keywords: Keywords that should appear in results
        retriever: Your LangChain retriever object
        k: Number of chunks to retrieve
        
    Returns:
        Tuple of (RetrievalMetrics, retrieved_chunks)
    """
    # Retrieve chunks
    retrieved_chunks = retriever.invoke(question)
    
    # Calculate MRR for each keyword, then average
    mrr_scores = []
    for keyword in expected_keywords:
        mrr = calculate_mrr(keyword, retrieved_chunks)
        mrr_scores.append(mrr)
    
    avg_mrr = sum(mrr_scores) / len(mrr_scores) if mrr_scores else 0.0
    
    # Calculate nDCG for each keyword, then average
    ndcg_scores = []
    for keyword in expected_keywords:
        ndcg = calculate_ndcg(keyword, retrieved_chunks, k)
        ndcg_scores.append(ndcg)
    
    avg_ndcg = sum(ndcg_scores) / len(ndcg_scores) if ndcg_scores else 0.0
    
    # Calculate keyword coverage
    keywords_found = sum(1 for score in mrr_scores if score > 0)
    total_keywords = len(expected_keywords)
    coverage = (keywords_found / total_keywords * 100) if total_keywords > 0 else 0.0
    
    metrics = RetrievalMetrics(
        mrr=avg_mrr,
        ndcg=avg_ndcg,
        keyword_coverage=coverage,
        keywords_found=keywords_found,
        total_keywords=total_keywords
    )
    
    return metrics, retrieved_chunks


# ============================================
# ANSWER EVALUATION
# ============================================

def evaluate_answer_manual(
    question: str,
    generated_answer: str,
    reference_answer: str
) -> AnswerMetrics:
    """
    Manual evaluation - you score the answer yourself.
    
    This is useful when starting out or for spot-checking.
    Later, you can use an LLM-as-judge for automation.
    
    Args:
        question: The question asked
        generated_answer: Answer from your RAG system
        reference_answer: The ideal/correct answer
        
    Returns:
        AnswerMetrics with your manual scores
    """
    print("\n" + "="*80)
    print("MANUAL EVALUATION")
    print("="*80)
    print(f"\nQuestion: {question}")
    print(f"\nReference Answer:\n{reference_answer}")
    print(f"\nGenerated Answer:\n{generated_answer}")
    print("\n" + "-"*80)
    
    # Prompt for manual scoring
    print("\nPlease evaluate the answer:")
    print("Rate from 1 (very poor) to 5 (perfect)")
    
    accuracy = float(input("Accuracy (factual correctness): "))
    completeness = float(input("Completeness (covers all aspects): "))
    relevance = float(input("Relevance (directly answers question): "))
    feedback = input("Feedback (optional): ")
    
    return AnswerMetrics(
        accuracy=accuracy,
        completeness=completeness,
        relevance=relevance,
        feedback=feedback or "Manual evaluation"
    )


def evaluate_answer_with_llm(
    question: str,
    generated_answer: str,
    reference_answer: str,
    llm
) -> AnswerMetrics:
    """
    Automated evaluation using LLM-as-a-judge.
    
    The LLM compares your answer to the reference answer.
    This is useful for batch evaluation of many questions.
    
    Args:
        question: The question asked
        generated_answer: Answer from your RAG system
        reference_answer: The ideal/correct answer
        llm: Your LLM instance (Ollama, OpenAI, etc.)
        
    Returns:
        AnswerMetrics with LLM's evaluation
    """
    judge_prompt = f"""You are an expert evaluator for a Korea study abroad consulting chatbot.

Question: {question}

Generated Answer:
{generated_answer}

Reference Answer:
{reference_answer}

Evaluate the generated answer on these 3 dimensions (scale 1-5):

1. ACCURACY: Is the information factually correct?
   - 5 = Perfect, all facts correct
   - 3 = Mostly correct with minor errors
   - 1 = Wrong or misleading information

2. COMPLETENESS: Does it cover all important points from reference?
   - 5 = All key information included
   - 3 = Main points covered, some details missing
   - 1 = Major information gaps

3. RELEVANCE: Does it directly answer the question?
   - 5 = Perfectly focused, no extra info
   - 3 = Answers question but includes unnecessary details
   - 1 = Off-topic or doesn't address question

Respond in this exact format:
ACCURACY: [score]
COMPLETENESS: [score]
RELEVANCE: [score]
FEEDBACK: [1-2 sentence explanation]"""

    # Get LLM evaluation
    response = llm.invoke(judge_prompt)
    response_text = response.content if hasattr(response, 'content') else str(response)
    
    # Parse the response
    lines = response_text.strip().split('\n')
    scores = {}
    feedback = ""
    
    for line in lines:
        if line.startswith("ACCURACY:"):
            scores['accuracy'] = float(line.split(':')[1].strip())
        elif line.startswith("COMPLETENESS:"):
            scores['completeness'] = float(line.split(':')[1].strip())
        elif line.startswith("RELEVANCE:"):
            scores['relevance'] = float(line.split(':')[1].strip())
        elif line.startswith("FEEDBACK:"):
            feedback = line.split(':', 1)[1].strip()
    
    return AnswerMetrics(
        accuracy=scores.get('accuracy', 3.0),
        completeness=scores.get('completeness', 3.0),
        relevance=scores.get('relevance', 3.0),
        feedback=feedback or response_text
    )


# ============================================
# BATCH EVALUATION
# ============================================

def run_full_evaluation(
    retriever,
    answer_function,
    use_manual_eval: bool = False,
    llm = None,
    test_file: str = "tests.jsonl"
):
    """
    Run evaluation on all test questions.
    
    Args:
        retriever: Your LangChain retriever
        answer_function: Function that takes (question, history) and returns answer
        use_manual_eval: If True, manually score each answer
        llm: LLM for automated evaluation (required if use_manual_eval=False)
        test_file: Path to test questions file
        
    Returns:
        Dictionary with results
    """
    tests = load_tests_from_jsonl(test_file)
    
    results = {
        'retrieval': [],
        'answers': [],
        'tests': []
    }
    
    print(f"\n{'='*80}")
    print(f"Running evaluation on {len(tests)} test questions")
    print(f"{'='*80}\n")
    
    for i, test in enumerate(tests, 1):
        print(f"\nTest {i}/{len(tests)}: {test.category}")
        print(f"Question: {test.question}")
        
        # Evaluate retrieval
        retrieval_metrics, chunks = evaluate_retrieval(
            test.question,
            test.keywords,
            retriever
        )
        
        print(f"  MRR: {retrieval_metrics.mrr:.3f}")
        print(f"  nDCG: {retrieval_metrics.ndcg:.3f}")
        print(f"  Coverage: {retrieval_metrics.keyword_coverage:.1f}%")
        
        # Generate answer
        generated_answer = answer_function(test.question, [])
        
        # Evaluate answer
        if use_manual_eval:
            answer_metrics = evaluate_answer_manual(
                test.question,
                generated_answer,
                test.reference_answer
            )
        else:
            if llm is None:
                raise ValueError("LLM required for automated evaluation")
            answer_metrics = evaluate_answer_with_llm(
                test.question,
                generated_answer,
                test.reference_answer,
                llm
            )
        
        print(f"  Accuracy: {answer_metrics.accuracy:.2f}/5")
        print(f"  Completeness: {answer_metrics.completeness:.2f}/5")
        print(f"  Relevance: {answer_metrics.relevance:.2f}/5")
        
        # Store results
        results['retrieval'].append(retrieval_metrics)
        results['answers'].append(answer_metrics)
        results['tests'].append(test)
    
    # Calculate averages
    avg_mrr = sum(r.mrr for r in results['retrieval']) / len(results['retrieval'])
    avg_ndcg = sum(r.ndcg for r in results['retrieval']) / len(results['retrieval'])
    avg_coverage = sum(r.keyword_coverage for r in results['retrieval']) / len(results['retrieval'])
    
    avg_accuracy = sum(a.accuracy for a in results['answers']) / len(results['answers'])
    avg_completeness = sum(a.completeness for a in results['answers']) / len(results['answers'])
    avg_relevance = sum(a.relevance for a in results['answers']) / len(results['answers'])
    
    print(f"\n{'='*80}")
    print("OVERALL RESULTS")
    print(f"{'='*80}")
    print("\nRetrieval Metrics:")
    print(f"  Average MRR: {avg_mrr:.3f}")
    print(f"  Average nDCG: {avg_ndcg:.3f}")
    print(f"  Average Coverage: {avg_coverage:.1f}%")
    print("\nAnswer Quality:")
    print(f"  Average Accuracy: {avg_accuracy:.2f}/5")
    print(f"  Average Completeness: {avg_completeness:.2f}/5")
    print(f"  Average Relevance: {avg_relevance:.2f}/5")
    
    results['summary'] = {
        'avg_mrr': avg_mrr,
        'avg_ndcg': avg_ndcg,
        'avg_coverage': avg_coverage,
        'avg_accuracy': avg_accuracy,
        'avg_completeness': avg_completeness,
        'avg_relevance': avg_relevance
    }
    
    return results


# ============================================
# CATEGORY ANALYSIS
# ============================================

def analyze_by_category(results):
    """
    Break down results by question category.
    
    This helps identify which types of questions your RAG handles well/poorly.
    """
    from collections import defaultdict
    
    categories = defaultdict(lambda: {'retrieval': [], 'answers': []})
    
    for i, test in enumerate(results['tests']):
        cat = test.category
        categories[cat]['retrieval'].append(results['retrieval'][i])
        categories[cat]['answers'].append(results['answers'][i])
    
    print(f"\n{'='*80}")
    print("RESULTS BY CATEGORY")
    print(f"{'='*80}\n")
    
    for category, data in categories.items():
        n = len(data['retrieval'])
        
        avg_mrr = sum(r.mrr for r in data['retrieval']) / n
        avg_accuracy = sum(a.accuracy for a in data['answers']) / n
        
        print(f"{category.upper()} ({n} questions):")
        print(f"  MRR: {avg_mrr:.3f}")
        print(f"  Accuracy: {avg_accuracy:.2f}/5")
        print()


if __name__ == "__main__":
    print("This module contains evaluation functions.")
    print("Import these functions in your main notebook to run evaluations.")