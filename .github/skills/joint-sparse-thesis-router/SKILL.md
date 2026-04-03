---
name: joint-sparse-thesis-router
description: "Use when user asks thesis replication tasks for Greedy Algorithms for Joint Sparse Recovery, including alignment gap scan, experiment protocol extraction, code structure design, result mismatch debugging, writing experiment analysis, defense prep, ARIP/phase transition explanation, or figure/caption drafting. Trigger keywords: 对齐, 差距, 偏题, 还缺什么, 原文实验配置, 参数怎么设, 停止准则, 帮我搭代码结构, 结果对不上, 图不对, 复现失败, 帮我写实验分析, 答辩准备, ARIP, 相变, caption."
---

# Joint Sparse Thesis Router

## Goal
Route short or ambiguous requests to the correct workflow so progress continues with minimal back-and-forth.

## Scope
Project: replication of "Greedy Algorithms for Joint Sparse Recovery".

## Routing Table
- Alignment / scope drift -> gap-scan workflow
- Experimental settings / protocol -> protocol-extraction workflow
- Coding architecture / implementation order -> code-cocreation workflow
- Result mismatch / unstable curves -> debugging workflow
- Writing analysis paragraphs -> results-writing workflow
- Defense rehearsal -> defense-prep workflow
- ARIP, RIP, strong/weak phase transition -> theory-compression workflow
- Figure recreation, axis explanation, caption -> figure-caption workflow

## Response Contract
When activated, respond in 4 parts only:
1. Current judgment (intent + assumptions)
2. Chosen workflow
3. Immediate executable output (3-5 actions or one ready-to-use prompt/template)
4. Next best single step

## Progressive Disclosure Rules
- Start with minimum executable output.
- Expand only after user asks for detail.
- Do not repeat confirmed background.
- Distinguish strictly:
  - What the target paper explicitly did
  - What the user has already completed
  - What is still planned

## Minimal Clarification Rule
Ask at most 1-2 questions only when blocked by missing artifacts (code/log/figure/section text). Otherwise proceed directly.
