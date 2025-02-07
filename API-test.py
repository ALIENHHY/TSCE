import os
from loguru import logger
from tqdm import tqdm
from together import Together
from openai import OpenAI

# 初始化 ChatGPT 客户端（用于评价摘要质量）
client_GPT = OpenAI(
    base_url='YOUR_BASE_URL',
    api_key='YOUR_API_KEY'
)

# 初始化 deepseek 客户端（用于生成摘要）
client_together = Together(
    base_url='YOUR_BASE_URL',
    api_key='YOUR_API_KEY'
)

# --- 定义生成摘要的函数 ---
def generate_summary(news_text, model="gpt-4o"):
    try:
        completion = client_GPT.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是一位资深新闻编辑，请帮我生成一份关于新闻的摘要，摘要需要尽可能地简介，使一眼就能了解大意。"},
                {"role": "user", "content": news_text}
            ]
        )
        # 假设返回结果在 completion.choices[0].message 中，将其转换为字符串
        summary = str(completion.choices[0].message)
        return summary
    except Exception as e:
        logger.error(f"DeepSeek 摘要生成失败: {e}")
        return ""

# --- 定义评价摘要质量的函数 ---
def evaluate_summary(news_text, summary, model="gpt-3.5-turbo"):
    try:
        prompt = (
            "以下是新闻原文与对应的摘要，请根据《大模型新闻摘要能力评价体系标准》对摘要进行严格评分，"
            "评价标准如下：\n"
            "1. 准确性：摘要是否正确反映了新闻的关键信息；\n"
            "2. 完整性：摘要是否涵盖了主要的事件、人物、时间和地点；\n"
            "3. 简洁性：摘要是否精炼，不冗余；\n"
            "4. 语言流畅度：摘要语言是否通顺、符合书面表达；\n"
            "5. 逻辑清晰度：摘要结构是否清晰、逻辑关系是否明确。\n\n"
            "请对每个维度进行评分（0～10分），最后计算各维度均等加权后的平均分作为最终评分。"
            "要求：\n"
            "- 评分必须在0～10之间；\n"
            "- 评分结果可以是整数或保留一位小数；\n"
            "- 返回的内容**仅**包含评分,包含五个维度的得分和最终评分，例如：'准确性：9分，完整性：8分，简洁性：9分，语言流畅度：9分，逻辑清晰度：8分，最终评分：8.6分'。\n\n"
            f"新闻原文：{news_text}\n\n摘要：{summary}\n\n"
            "请严格按照上述要求返回最终评分。"
        )
        completion = client_GPT.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是一位资深新闻编辑，熟悉新闻摘要评价标准。请根据给定标准对摘要进行严格打分。"},
                {"role": "user", "content": prompt}
            ]
        )
        evaluation = str(completion.choices[0].message)
        return evaluation
    except Exception as e:
        logger.error(f"ChatGPT 评价摘要失败: {e}")
        return ""


# --- 定义加载新闻数据集的函数 ---
def load_news_dataset(file_path: str) -> list:
    """
    从指定文件中加载新闻数据。
    每一行应包含“正文：”后面的新闻文本。
    返回的每条记录为一个字典，包含 'ID' 和 'text' 字段。
    """
    dataset = []
    if not os.path.exists(file_path):
        logger.error(f"文件 {file_path} 不存在！")
        return dataset
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
    for idx, line in enumerate(lines):
        if "正文：" in line:
            parts = line.split("正文：", 1)
            news_text = parts[1].strip()
        else:
            news_text = line.strip()
        dataset.append({"ID": str(idx + 1), "text": news_text})
    return dataset

# --- 定义评估新闻摘要的主函数 ---
def evaluate_news_summaries(file_path="1.txt", output_path="result.txt") -> list:
    dataset = load_news_dataset(file_path)
    results = []
    for item in tqdm(dataset, desc="处理新闻"):
        news_text = item["text"]
        summary = generate_summary(news_text)
        evaluation = evaluate_summary(news_text, summary)
        results.append({
            "ID": item["ID"],
            "news_text": news_text,
            "summary": summary,
            "evaluation": evaluation
        })
    # 将结果写入 TXT 文件，每条新闻按固定格式写入
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            for item in results:
                f.write(f"ID: {item['ID']}\n")
                f.write("新闻摘要:\n")
                f.write(f"{item['summary']}\n\n")
                f.write("评价:\n")
                f.write(f"{item['evaluation']}\n")
                f.write("\n" + "="*50 + "\n\n")
    except Exception as e:
        logger.error(f"保存结果到 TXT 文件失败: {e}")
    return results

# --- 主程序入口 ---
if __name__ == "__main__":
    results = evaluate_news_summaries("data-tset.txt")
    print("评估完成，结果已保存")
