---
title: "How to run the "
permalink: /docs/how-to-setup-llm-proxy-project/
excerpt: "How to quickly install and setup Prompt Sail project."
last_modified_at: 2023-12-22T18:48:05+01:00
redirect_from:
  - /theme-setup/
toc: true
---





**Configuration**

The setup is straightforward. You need to modify the `base_url` when creating your AI API object. 
You can also include additional parameters in the URL, such as `project_slug`, `provider_slug`, and `tags`.
__Tags are not required.__

Here's a template for the `base_url` when you don't want to tag your transactions:

```
http://localhost:8000/<project_slug>/<provider_slug>/chat/completions
```

However, if you are interested in tagging your transactions you need to build a link as follows:

```
http://localhost:8000/<project_slug>/<provider_slug>/?tags=zero_shot,simple_prompt,dev1,poc&target_path=/chat/completions
```

As you can see right after `provider_slug` the tags immediately appear, and then as query_param `target_path` we added 
the rest of the link. If you use most libraries, you should leave this parameter empty, ie: `target_path=`, 
because they add the rest of the link themselves. 

**Usage**

Once the setup is complete, you can begin using Prompt Sail. It will automatically capture and log all prompts and responses. You can then view and analyze this data through the intuitive user interface. UI is available at [http://localhost:80/](http://localhost:80/)

Prompt Sail is designed to integrate smoothly into your workflow, offering valuable insights without causing any disruption to your development process.
