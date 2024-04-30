---
layout: splash
permalink: /
hidden: true
header:
    overlay_color: "#38928d"
    overlay_filter: "0.3 0.1"
    overlay_image: /assets/images/home-page-feature-bckg.png
    actions:
        - label: "<i class='fas fa-solid fa-code'></i> Try now"
          url: "/docs/quick-start-guide/"
excerpt: >
    LLM's proxy for prompt and response governance, monitoring, and cost analysis.<br />
    <small><a href="https://github.com/PromptSail/prompt_sail/releases/">Latest release</a></small>
intro:
    - excerpt: "Prompt Sail is a transparent and user-friendly tool designed to capture and log all interactions with LLM APIs such as OpenAI, Cohere, and others. It integrates with OpenAI, langchain, and other LLM frameworks and libraries."
feature_row:
    - image_path: #/assets/images/mm-customizable-feature.png
      alt: "Easy Integration"
      title: "Easy Integration"
      excerpt: "Engineered as a transparent Proxy for your LLM calls, it seamlessly integrates into your existing workflow, and your LLM framework."
      url: "/docs/quick-start-guide/"
      btn_class: "btn--primary"
      btn_label: "Learn more"
    - image_path: #/assets/images/mm-responsive-feature.png
      alt: "fully responsive"
      title: "Cost Monitoring"
      excerpt: "Provides a comprehensive dashboard for tracking your usage and budgeting your LLM API calls."
      url: "/docs/layouts/"
      btn_class: "btn--primary"
      btn_label: "Learn more"
    - image_path: #/assets/images/mm-free-feature.png
      alt: "100% free and MIT licensed"
      title: "100% free"
      excerpt: "Free to use however you want under the MIT License. Clone it, fork it, customize it... whatever!"
      url: "/docs/license/"
      btn_class: "btn--primary"
      btn_label: "Learn more"
---

{% include feature_row %}

![LLM deployments project dashboards with charts: budgets and transactions]({{ site.url }}{{ site.baseurl }}assets/images/LLM_Project_dashboard_budget.png){: .align-center}


## What is Prompt Sail?

1. **Transparent Logging** 
It captures and logs all interactions with LLM APIs, providing a comprehensive record of prompts and responses.

2. **Cost Insights** 
Project managers can track and analyze the costs associated with each project and experiment, enabling better budget management.

3. **Optimization and Analysis**
By providing a concise and detailed view of all interactions, developers can analyze and refine their prompts.

4. **Compliance and Governance**
Empowers business owners to maintain control over instructions, chat messages, and other interactions with LLM APIs. This enables the implementation of standards and policies, identification of misuse, and detection of non-compliant content.

5. **Easy Integration** 
Prompt Sail seamlessly integrates into your workflow and used libraries. Just modify the `base_url` parameter when creating your provider API object.

6. **Searchable Database**
All prompts and responses are stored in a MongoDB, making finding and analyzing specific interactions easy. You can export the data for further analysis.

7. **User-Friendly Interface**
Simple and intuitive UI lets you easily view and filter your transactions (prompts and responses) by project, API provider, LLM model, or tags.


