#!/usr/bin/env python3
"""Insert SVG diagrams into the presentation HTML."""

import re

HTML_PATH = '/Users/hanuma/presentations/ai-architectures/index.html'
DIAGRAM_DIR = 'diagrams'

# Mapping of slide titles (or patterns) to diagram filenames
DIAGRAM_INSERTIONS = [
    # Section II: Transformer
    (r'<h2>Transformer Architecture Overview</h2>\s*<div class="two-column">', 
     'transformer', 'Transformer Architecture (Vaswani et al., 2017)'),
    (r'<h2>Self-Attention: The Core Mechanism</h2>\s*<div class="two-column">',
     'self_attention', 'Scaled Dot-Product Attention'),
    (r'<h2>Multi-Head Attention</h2>\s*<div class="two-column">',
     'multihead_attention', 'Multi-Head Attention'),
    
    # Section III: Transformer Variants
    (r'<h2>BERT: Bidirectional Encoder \(2018\)</h2>\s*<div class="two-column">',
     'bert', 'BERT Architecture'),
    (r'<h2>GPT Series: Generative Pre-Training</h2>\s*<div class="two-column">',
     'gpt', 'GPT Decoder-Only Architecture'),
    (r'<h2>T5: Text-to-Text Transfer Transformer</h2>\s*<div class="two-column">',
     't5', 'T5 Encoder-Decoder Architecture'),
    
    # Section IV: Scaling
    (r'<h2>LLaMA: Open Foundation Models</h2>\s*<div class="two-column">',
     'llama', 'LLaMA Architecture'),
    
    # Section V: MoE
    (r'<h2>What is Mixture of Experts\?</h2>\s*<div class="two-column">',
     'moe', 'Mixture of Experts Routing'),
    
    # Section VI: Multi-Modal
    (r'<h2>CLIP: Contrastive Language-Image Pre-training</h2>\s*<div class="two-column">',
     'clip', 'CLIP Dual Encoder Architecture'),
    (r'<h2>Vision Transformer \(ViT\)</h2>\s*<div class="two-column">',
     'vit', 'Vision Transformer (ViT)'),
    (r'<h2>Stable Diffusion Architecture</h2>\s*<div class="two-column">',
     'stable_diffusion', 'Latent Diffusion Model (Stable Diffusion)'),
    (r'<h2>Whisper Architecture</h2>\s*<div class="two-column">',
     'whisper', 'Whisper Encoder-Decoder Architecture'),
    
    # Section VII: Vision
    (r'<h2>DETR: Detection Transformer</h2>\s*<div class="two-column">',
     None, None),  # Skip, not generated
    (r'<h2>SAM: Segment Anything Model</h2>\s*<div class="two-column">',
     None, None),
    
    # Section VIII: Efficient
    (r'<h2>Mamba: Selective State Spaces</h2>\s*<div class="two-column">',
     'mamba', 'Mamba Selective State Space Model'),
    
    # Section IX: Generative
    (r'<h2>Variational Autoencoder \(VAE\)</h2>\s*<div class="two-column">',
     'vae', 'VAE: Variational Autoencoder'),
    (r'<h2>Generative Adversarial Networks \(GANs\)</h2>\s*<div class="two-column">',
     'gan', 'GAN: Generative Adversarial Network'),
    (r'<h2>Diffusion Models: Foundations</h2>\s*<div class="two-column">',
     'diffusion_process', 'Diffusion Forward & Reverse Process'),
    
    # Section X: Training
    (r'<h2>RLHF: Reinforcement Learning from Human Feedback</h2>\s*<div class="two-column">',
     'rlhf', 'RLHF Pipeline'),
    (r'<h2>DPO: Direct Preference Optimization</h2>\s*<div class="two-column">',
     'dpo', 'DPO: Direct Preference Optimization'),
    (r'<h2>Test-Time Compute Scaling \(o1/o3\)</h2>\s*<div class="two-column">',
     'test_time_compute', 'Test-Time Compute Scaling'),
    
    # Section XI: Retrieval
    (r'<h2>RAG: Retrieval-Augmented Generation</h2>\s*<div class="two-column">',
     'rag', 'RAG Architecture'),
    
    # Section XII: Agents
    (r'<h2>ReAct: Reasoning \+ Acting</h2>\s*<div class="two-column">',
     'react', 'ReAct: Reasoning + Acting'),
    (r'<h2>Reflexion: Self-Reflective Agents</h2>\s*<div class="two-column">',
     None, None),
    
    # Section XIII: Systems
    # None for now
    
    # Additional foundation slides
    (r'<h2>ResNet: Residual Learning</h2>\s*<div class="two-column">',
     'resnet', 'ResNet Residual Block'),
    (r'<h2>LSTM &amp; GRU: Gated Recurrent Units</h2>\s*<div class="two-column">',
     'lstm', 'LSTM Cell'),
    (r'<h2>Convolutional Neural Networks \(CNNs\)</h2>\s*<div class="two-column">',
     'cnn', 'CNN Architecture'),
]

def insert_diagram(html, pattern, diagram_name, caption):
    if diagram_name is None:
        return html
    
    img_tag = f'<div style="text-align:center; margin: 1em 0;"><img src="{DIAGRAM_DIR}/{diagram_name}.svg" style="max-width: 85%; max-height: 500px; border-radius: 8px;" alt="{caption}"><p style="font-size: 0.7em; color: #888; margin-top: 0.5em;">{caption}</p></div>'
    
    # Find the section that matches the pattern
    match = re.search(pattern, html)
    if not match:
        print(f"Warning: Pattern not found for {diagram_name}")
        return html
    
    # Insert the image BEFORE the matched content
    pos = match.start()
    html = html[:pos] + img_tag + '\n            ' + html[pos:]
    print(f"Inserted: {diagram_name}.svg")
    return html

def main():
    with open(HTML_PATH, 'r') as f:
        html = f.read()
    
    for pattern, diagram_name, caption in DIAGRAM_INSERTIONS:
        html = insert_diagram(html, pattern, diagram_name, caption)
    
    with open(HTML_PATH, 'w') as f:
        f.write(html)
    
    print("Done! All diagrams inserted.")

if __name__ == '__main__':
    main()
