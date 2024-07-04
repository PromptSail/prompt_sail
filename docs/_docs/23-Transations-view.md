---
title: "Transations View"
permalink: /docs/transations-view
excerpt: "The Transactions View page provides detailed information about a specific project's transactions."
last_modified_at: 2024-07-01T15:36:00+01:00
redirect_from:
    - /theme-setup/
toc: true
toc_sticky: true
---



## Transactions Overview
The **Transactions View** provides a detailed log of each transaction made across your projects. Filter and sort transactions by various criteria, such as time, speed, status, project, AI provider, model, tags, cost, and tokens. This view allows you to browse through all captured historical interactions.

![PromptSail UI GenAI transation table view]({{ site.url }}{{ site.baseurl }}assets/images/prompsail_ui_transations_view.png){: .align-center}

### Transactions Table
A table displaying all transactions with the following details:
- **ID**: Unique identifier for each transaction.
- **Time**: Timestamp of when the transaction was initiated.
- **Speed**: Response speed measured in tokens per second.
- **Messages**: Shows both the input and output of each transaction.
- **Status**: The HTTP status code of the transaction (e.g., 200 for successful transactions, 401 for unauthorized access).
- **Project**: The specific project to which the transaction belongs.
- **AI Provider**: The AI service provider used for the transaction.
- **Model**: The machine learning model used.
- **Tags**: Any tags associated with the transaction for easy categorization.
- **Cost**: The cost incurred for the transaction.
- **Tokens**: Number of tokens used, showing initial and


