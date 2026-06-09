#!/usr/bin/env python3
"""Generate architecture diagrams replicating original paper figures."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

plt.rcParams['figure.facecolor'] = '#1a1a2e'
plt.rcParams['axes.facecolor'] = '#1a1a2e'
plt.rcParams['text.color'] = '#eaeaea'
plt.rcParams['axes.labelcolor'] = '#eaeaea'
plt.rcParams['xtick.color'] = '#eaeaea'
plt.rcParams['ytick.color'] = '#eaeaea'

OUTPUT_DIR = '/Users/hanuma/presentations/ai-architectures/diagrams'

def save_svg(fig, name):
    fig.savefig(f'{OUTPUT_DIR}/{name}.svg', format='svg', bbox_inches='tight', 
                facecolor='#1a1a2e', edgecolor='none', pad_inches=0.1)
    plt.close(fig)

def add_box(ax, x, y, w, h, text, color='#2d2d44', text_color='#eaeaea', fontsize=9, style='round'):
    if style == 'round':
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.15",
                             facecolor=color, edgecolor='#555', linewidth=1.5)
    else:
        box = plt.Rectangle((x, y), w, h, facecolor=color, edgecolor='#555', linewidth=1.5)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=fontsize,
            color=text_color, fontweight='bold', wrap=True)
    return box

def add_arrow(ax, x1, y1, x2, y2, color='#00d4aa'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5))

def setup_ax(ax, title=None):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold', color='#00d4aa', pad=10)

# ============================================================================
# 1. ORIGINAL TRANSFORMER (Vaswani et al. 2017)
# ============================================================================
def draw_transformer():
    fig, ax = plt.subplots(1, 1, figsize=(10, 14))
    setup_ax(ax, 'Transformer Architecture (Vaswani et al., 2017)')
    
    # Encoder stack (left)
    ex = 1.5
    add_box(ax, ex, 8.5, 3, 0.8, 'Input Embedding', '#1565c0')
    add_box(ax, ex, 7.5, 3, 0.6, '+ Positional Encoding', '#455a64', fontsize=8)
    
    # Encoder layers (stack of N)
    for i in range(3):
        y = 6.2 - i*1.8
        add_box(ax, ex, y+0.9, 3, 0.7, 'Multi-Head Attention', '#c62828')
        add_box(ax, ex+1.2, y+0.4, 0.8, 0.35, 'Add & Norm', '#455a64', fontsize=7)
        add_box(ax, ex, y, 3, 0.7, 'Feed Forward', '#ef6c00')
        add_box(ax, ex+1.2, y-0.5, 0.8, 0.35, 'Add & Norm', '#455a64', fontsize=7)
        if i < 2:
            add_arrow(ax, ex+1.5, y-0.5, ex+1.5, y+0.9+0.7+0.1)
    
    ax.text(ex+1.5, 5.5, 'Nx', ha='center', va='center', fontsize=12, color='#888', style='italic')
    
    # Decoder stack (right)
    dx = 5.5
    add_box(ax, dx, 8.5, 3, 0.8, 'Output Embedding', '#1565c0')
    add_box(ax, dx, 7.5, 3, 0.6, '+ Positional Encoding', '#455a64', fontsize=8)
    
    for i in range(3):
        y = 6.2 - i*1.8
        add_box(ax, dx, y+0.9, 3, 0.7, 'Masked Multi-Head Attention', '#c62828')
        add_box(ax, dx+1.2, y+0.4, 0.8, 0.35, 'Add & Norm', '#455a64', fontsize=7)
        add_box(ax, dx, y, 3, 0.7, 'Multi-Head Attention', '#c62828')
        add_box(ax, dx+1.2, y-0.5, 0.8, 0.35, 'Add & Norm', '#455a64', fontsize=7)
        add_box(ax, dx, y-1.2, 3, 0.7, 'Feed Forward', '#ef6c00')
        if i < 2:
            add_arrow(ax, dx+1.5, y-1.2, dx+1.5, y+0.9+0.7+0.1)
    
    ax.text(dx+1.5, 5.5, 'Nx', ha='center', va='center', fontsize=12, color='#888', style='italic')
    
    # Cross-attention arrows from encoder to decoder
    for yd in [5.3, 3.5]:
        ax.annotate('', xy=(dx, yd), xytext=(ex+3, yd),
                    arrowprops=dict(arrowstyle='->', color='#4fc3f7', lw=1.5,
                                    connectionstyle="arc3,rad=0.1"))
    
    # Output
    add_box(ax, dx, 0.3, 3, 0.6, 'Linear + Softmax', '#2e7d32')
    add_arrow(ax, dx+1.5, 0.9, dx+1.5, 1.5)
    add_box(ax, dx, 1.5, 3, 0.6, 'Output Probabilities', '#2e7d32')
    
    # Labels
    ax.text(ex+1.5, 9.7, 'ENCODER', ha='center', va='center', fontsize=11, 
            color='#4fc3f7', fontweight='bold')
    ax.text(dx+1.5, 9.7, 'DECODER', ha='center', va='center', fontsize=11, 
            color='#ff8a65', fontweight='bold')
    
    save_svg(fig, 'transformer')

# ============================================================================
# 2. SELF-ATTENTION MECHANISM
# ============================================================================
def draw_self_attention():
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    setup_ax(ax, 'Scaled Dot-Product Attention')
    
    # Input matrices
    add_box(ax, 0.5, 6.5, 2, 0.8, 'Q (Queries)', '#1565c0')
    add_box(ax, 0.5, 5.2, 2, 0.8, 'K (Keys)', '#1565c0')
    add_box(ax, 0.5, 3.9, 2, 0.8, 'V (Values)', '#1565c0')
    
    # QK^T
    add_arrow(ax, 1.5, 6.5, 3.5, 5.8)
    add_arrow(ax, 1.5, 5.6, 3.5, 5.5)
    add_box(ax, 3.5, 5.2, 2.5, 0.9, 'QK^T / sqrt(d_k)', '#6a1b9a')
    
    # Softmax
    add_arrow(ax, 4.75, 5.2, 4.75, 4.5)
    add_box(ax, 3.5, 3.8, 2.5, 0.6, 'Softmax', '#6a1b9a')
    
    # Multiply with V
    add_arrow(ax, 4.75, 3.8, 4.75, 3.2)
    add_box(ax, 3.5, 2.5, 2.5, 0.6, 'x V', '#6a1b9a')
    add_arrow(ax, 1.5, 4.3, 3.5, 2.9)
    
    # Output
    add_arrow(ax, 4.75, 2.5, 4.75, 1.8)
    add_box(ax, 3.5, 1.0, 2.5, 0.7, 'Attention Output', '#2e7d32')
    
    # Mask option
    add_box(ax, 0.3, 2.5, 1.5, 0.5, 'Mask (opt)', '#455a64', fontsize=8)
    add_arrow(ax, 1.05, 3.0, 3.5, 3.5)
    
    save_svg(fig, 'self_attention')

# ============================================================================
# 3. MULTI-HEAD ATTENTION
# ============================================================================
def draw_multihead_attention():
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    setup_ax(ax, 'Multi-Head Attention')
    
    # Input
    add_box(ax, 0.3, 4.0, 1.5, 1.0, 'Input', '#1565c0')
    
    # Linear projections
    for i, label in enumerate(['W^Q', 'W^K', 'W^V']):
        x = 2.2 + i*0.7
        add_box(ax, x, 5.2, 0.5, 0.6, label, '#455a64', fontsize=8)
        add_box(ax, x, 3.2, 0.5, 0.6, label, '#455a64', fontsize=8)
        add_box(ax, x, 4.2, 0.5, 0.6, label, '#455a64', fontsize=8)
        add_arrow(ax, 1.8, 4.5, x+0.25, 5.2)
        add_arrow(ax, 1.8, 4.5, x+0.25, 4.5)
        add_arrow(ax, 1.8, 4.5, x+0.25, 3.5)
    
    # Attention heads
    for i in range(4):
        x = 5.0 + i*0.9
        add_box(ax, x, 4.0, 0.7, 1.0, f'h{i+1}', '#c62828', fontsize=9)
        add_arrow(ax, 4.5, 5.0, x+0.35, 4.8)
        add_arrow(ax, 4.5, 4.5, x+0.35, 4.5)
        add_arrow(ax, 4.5, 4.0, x+0.35, 4.2)
    
    # Concat + Linear
    add_box(ax, 5.0, 2.3, 3.4, 0.6, 'Concat', '#6a1b9a')
    for i in range(4):
        add_arrow(ax, 5.35+i*0.9, 4.0, 5.35+i*0.9, 2.9)
    
    add_arrow(ax, 6.7, 2.3, 6.7, 1.6)
    add_box(ax, 5.8, 0.8, 1.8, 0.7, 'W^O', '#6a1b9a')
    add_arrow(ax, 6.7, 0.8, 6.7, 0.2)
    add_box(ax, 5.5, -0.8, 2.4, 0.8, 'Output', '#2e7d32')
    
    save_svg(fig, 'multihead_attention')

# ============================================================================
# 4. BERT ARCHITECTURE
# ============================================================================
def draw_bert():
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    setup_ax(ax, 'BERT: Bidirectional Encoder (Devlin et al., 2018)')
    
    # Input
    add_box(ax, 1.0, 8.0, 8, 0.7, '[CLS] tok1 tok2 [MASK] tok4 ... [SEP]', '#1565c0')
    add_box(ax, 1.0, 7.1, 8, 0.6, 'Token Embeddings + Segment Embeddings + Position Embeddings', '#455a64', fontsize=8)
    
    # Transformer blocks
    for i in range(4):
        y = 5.8 - i*1.3
        add_box(ax, 1.0, y+0.6, 8, 0.6, 'Multi-Head Attention (Bidirectional)', '#c62828')
        add_box(ax, 4.2, y+0.15, 1.6, 0.35, 'Add & Norm', '#455a64', fontsize=8)
        add_box(ax, 1.0, y, 8, 0.6, 'Feed Forward Network', '#ef6c00')
        add_box(ax, 4.2, y-0.45, 1.6, 0.35, 'Add & Norm', '#455a64', fontsize=8)
        if i < 3:
            ax.annotate('', xy=(5, y-0.45), xytext=(5, y+0.6+0.7),
                       arrowprops=dict(arrowstyle='->', color='#888', lw=1))
    
    ax.text(5, 4.3, 'x12 (BERT-Base)', ha='center', va='center', fontsize=10, color='#888', style='italic')
    
    # Output heads
    add_box(ax, 0.5, 1.0, 3.5, 0.7, 'MLM Head\n(Predict [MASK])', '#2e7d32')
    add_box(ax, 6.0, 1.0, 3.5, 0.7, 'NSP Head\n(Next Sentence?)', '#2e7d32')
    add_arrow(ax, 3.0, 1.7, 2.25, 2.3)
    add_arrow(ax, 7.0, 1.7, 7.75, 2.3)
    
    save_svg(fig, 'bert')

# ============================================================================
# 5. GPT DECODER-ONLY
# ============================================================================
def draw_gpt():
    fig, ax = plt.subplots(1, 1, figsize=(8, 10))
    setup_ax(ax, 'GPT: Decoder-Only Architecture')
    
    add_box(ax, 1.5, 8.5, 7, 0.7, 'Input Tokens', '#1565c0')
    add_box(ax, 1.5, 7.6, 7, 0.6, 'Token + Position Embeddings', '#455a64', fontsize=9)
    
    for i in range(4):
        y = 6.4 - i*1.4
        add_box(ax, 1.5, y+0.5, 7, 0.6, 'Masked Multi-Head Self-Attention', '#c62828')
        add_box(ax, 4.2, y+0.1, 1.6, 0.3, 'Add & Norm', '#455a64', fontsize=8)
        add_box(ax, 1.5, y-0.4, 7, 0.6, 'Feed Forward Network', '#ef6c00')
        add_box(ax, 4.2, y-0.8, 1.6, 0.3, 'Add & Norm', '#455a64', fontsize=8)
        if i < 3:
            ax.annotate('', xy=(5, y-0.8), xytext=(5, y+0.5+0.7),
                       arrowprops=dict(arrowstyle='->', color='#888', lw=1))
    
    ax.text(5, 4.2, 'xN (12-96+ layers)', ha='center', va='center', fontsize=10, color='#888', style='italic')
    
    add_box(ax, 1.5, 0.8, 7, 0.7, 'LayerNorm + Language Modeling Head', '#2e7d32')
    add_arrow(ax, 5, 1.5, 5, 2.2)
    add_box(ax, 1.5, -0.2, 7, 0.7, 'Next Token Probability Distribution', '#2e7d32')
    
    save_svg(fig, 'gpt')

# ============================================================================
# 6. T5 ENCODER-DECODER
# ============================================================================
def draw_t5():
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    setup_ax(ax, 'T5: Text-to-Text Transfer Transformer')
    
    # Encoder
    ex = 0.8
    add_box(ax, ex, 8.5, 4, 0.6, 'Input: "translate: Hello"', '#1565c0')
    
    for i in range(3):
        y = 7.2 - i*1.3
        add_box(ax, ex, y+0.5, 4, 0.6, 'Self-Attention', '#c62828')
        add_box(ax, ex, y-0.2, 4, 0.6, 'FFN', '#ef6c00')
        if i < 2:
            ax.annotate('', xy=(ex+2, y-0.2), xytext=(ex+2, y+0.5+0.7),
                       arrowprops=dict(arrowstyle='->', color='#888', lw=1))
    
    ax.text(ex+2, 5.5, 'Encoder', ha='center', va='center', fontsize=11, 
            color='#4fc3f7', fontweight='bold')
    
    # Decoder
    dx = 5.2
    add_box(ax, dx, 8.5, 4, 0.6, 'Output: "Bonjour"', '#1565c0')
    
    for i in range(3):
        y = 7.2 - i*1.3
        add_box(ax, dx, y+0.5, 4, 0.6, 'Masked Self-Attention', '#c62828')
        add_box(ax, dx, y, 4, 0.4, 'Cross-Attention', '#ff8a65')
        add_box(ax, dx, y-0.5, 4, 0.4, 'FFN', '#ef6c00')
        if i < 2:
            ax.annotate('', xy=(dx+2, y-0.5), xytext=(dx+2, y+0.5+0.7),
                       arrowprops=dict(arrowstyle='->', color='#888', lw=1))
    
    ax.text(dx+2, 5.5, 'Decoder', ha='center', va='center', fontsize=11, 
            color='#ff8a65', fontweight='bold')
    
    # Cross attention arrows
    for y in [6.2, 4.9]:
        ax.annotate('', xy=(dx, y), xytext=(ex+4, y),
                   arrowprops=dict(arrowstyle='->', color='#4fc3f7', lw=1.5,
                                  connectionstyle="arc3,rad=0.1"))
    
    save_svg(fig, 't5')

# ============================================================================
# 7. MIXTURE OF EXPERTS
# ============================================================================
def draw_moe():
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    setup_ax(ax, 'Mixture of Experts (MoE) Routing')
    
    add_box(ax, 0.5, 7.5, 2.5, 0.8, 'Input Token x', '#1565c0')
    add_arrow(ax, 1.75, 7.5, 1.75, 6.8)
    
    add_box(ax, 0.5, 6.0, 2.5, 0.7, 'Router / Gate', '#6a1b9a')
    add_arrow(ax, 1.75, 6.0, 1.75, 5.3)
    
    add_box(ax, 0.2, 4.5, 3.0, 0.7, 'Top-K Selection', '#6a1b9a')
    
    # Experts
    experts = ['Expert 1', 'Expert 2', 'Expert 3', 'Expert 4', '...', 'Expert E']
    for i, name in enumerate(experts):
        x = 4.0 + (i % 3) * 1.8
        y = 5.5 if i < 3 else 3.5
        add_box(ax, x, y, 1.5, 0.8, name, '#ef6c00', fontsize=8)
    
    # Router to experts arrows
    for i in range(3):
        add_arrow(ax, 3.2, 4.8, 4.0+i*1.8, 5.5+0.8)
    
    # Selected experts highlighted
    add_box(ax, 4.0, 5.5, 1.5, 0.8, 'Expert 1', '#2e7d32', fontsize=8)
    add_box(ax, 5.8, 5.5, 1.5, 0.8, 'Expert 2', '#2e7d32', fontsize=8)
    
    # Combine
    for x in [4.75, 6.55]:
        add_arrow(ax, x, 5.5, 5.5, 3.0)
    
    add_box(ax, 4.5, 2.2, 2.0, 0.7, 'Weighted Sum', '#6a1b9a')
    add_arrow(ax, 5.5, 2.2, 5.5, 1.5)
    add_box(ax, 4.0, 0.7, 3.0, 0.7, 'Output y', '#2e7d32')
    
    save_svg(fig, 'moe')

# ============================================================================
# 8. VISION TRANSFORMER
# ============================================================================
def draw_vit():
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    setup_ax(ax, 'Vision Transformer (ViT) - Dosovitskiy et al., 2020')
    
    # Image
    img = plt.Rectangle((0.5, 6.5), 2, 2, facecolor='#1565c0', edgecolor='#555', linewidth=2)
    ax.add_patch(img)
    ax.text(1.5, 7.5, 'Image\n224x224', ha='center', va='center', fontsize=9, color='white')
    
    # Patches
    patch_colors = ['#1e88e5', '#42a5f5', '#64b5f6', '#90caf9']
    px, py = 3.5, 6.5
    for i in range(4):
        for j in range(4):
            p = plt.Rectangle((px + j*0.5, py + i*0.5), 0.5, 0.5, 
                             facecolor=patch_colors[(i+j)%4], edgecolor='white', linewidth=1)
            ax.add_patch(p)
    ax.text(px+1.0, py+2.3, '16x16 Patches', ha='center', va='center', fontsize=8, color='#eaeaea')
    
    add_arrow(ax, 2.5, 7.5, 3.5, 7.5)
    add_arrow(ax, 5.5, 7.5, 6.5, 7.5)
    
    # Linear projection
    add_box(ax, 6.5, 7.0, 3, 0.8, 'Linear Projection\n(Embedding)', '#6a1b9a', fontsize=9)
    
    add_arrow(ax, 8.0, 7.0, 8.0, 6.2)
    
    # Transformer encoder
    add_box(ax, 6.5, 5.0, 3, 1.0, 'Transformer Encoder\nxL', '#c62828')
    
    # CLS and position
    add_box(ax, 6.0, 6.2, 0.8, 0.6, '[CLS]', '#ef6c00', fontsize=9)
    add_arrow(ax, 6.4, 6.2, 6.5, 5.8)
    add_box(ax, 9.0, 6.2, 0.8, 0.6, 'Pos', '#ef6c00', fontsize=9)
    add_arrow(ax, 9.0, 6.2, 8.5, 5.8)
    
    add_arrow(ax, 8.0, 5.0, 8.0, 4.2)
    add_box(ax, 6.5, 3.5, 3, 0.6, 'MLP Head', '#2e7d32')
    add_arrow(ax, 8.0, 3.5, 8.0, 2.7)
    add_box(ax, 6.5, 2.0, 3, 0.6, 'Classification', '#2e7d32')
    
    save_svg(fig, 'vit')

# ============================================================================
# 9. CLIP
# ============================================================================
def draw_clip():
    fig, ax = plt.subplots(1, 1, figsize=(10, 7))
    setup_ax(ax, 'CLIP: Contrastive Language-Image Pre-training')
    
    # Image encoder
    add_box(ax, 0.5, 5.5, 2.5, 0.8, 'Image', '#1565c0')
    add_arrow(ax, 1.75, 5.5, 1.75, 4.8)
    add_box(ax, 0.5, 4.0, 2.5, 0.7, 'Image Encoder\n(ViT or ResNet)', '#c62828')
    add_arrow(ax, 1.75, 4.0, 1.75, 3.3)
    add_box(ax, 0.5, 2.5, 2.5, 0.7, 'Image Embedding', '#2e7d32')
    
    # Text encoder
    add_box(ax, 7.0, 5.5, 2.5, 0.8, 'Text', '#1565c0')
    add_arrow(ax, 8.25, 5.5, 8.25, 4.8)
    add_box(ax, 7.0, 4.0, 2.5, 0.7, 'Text Encoder\n(Transformer)', '#c62828')
    add_arrow(ax, 8.25, 4.0, 8.25, 3.3)
    add_box(ax, 7.0, 2.5, 2.5, 0.7, 'Text Embedding', '#2e7d32')
    
    # Similarity matrix
    ax.annotate('', xy=(7.0, 2.9), xytext=(3.0, 2.9),
               arrowprops=dict(arrowstyle='<->', color='#ff8a65', lw=2))
    ax.text(5.0, 3.3, 'Cosine Similarity', ha='center', va='center', 
            fontsize=10, color='#ff8a65', fontweight='bold')
    
    # Contrastive loss
    add_box(ax, 3.5, 1.0, 3, 0.8, 'Contrastive Loss', '#6a1b9a')
    add_arrow(ax, 1.75, 2.5, 3.5, 1.5)
    add_arrow(ax, 8.25, 2.5, 6.5, 1.5)
    
    save_svg(fig, 'clip')

# ============================================================================
# 10. STABLE DIFFUSION
# ============================================================================
def draw_stable_diffusion():
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    setup_ax(ax, 'Latent Diffusion Model (Stable Diffusion)')
    
    add_box(ax, 0.5, 7.0, 2.5, 0.7, 'Text Prompt', '#1565c0')
    add_arrow(ax, 1.75, 7.0, 1.75, 6.3)
    add_box(ax, 0.5, 5.5, 2.5, 0.7, 'CLIP Text Encoder', '#c62828')
    add_arrow(ax, 1.75, 5.5, 1.75, 4.8)
    add_box(ax, 0.5, 4.0, 2.5, 0.7, 'Text Embeddings', '#6a1b9a')
    
    # Cross attention to UNet
    add_arrow(ax, 3.0, 4.3, 4.5, 4.3)
    
    add_box(ax, 4.5, 3.5, 3, 1.2, 'U-Net\n(Cross-Attention + ResBlocks)', '#c62828')
    
    add_arrow(ax, 4.5, 4.0, 3.0, 4.0)
    
    # Noise
    add_box(ax, 4.0, 6.5, 2, 0.6, 'Random Noise z_T', '#1565c0')
    add_arrow(ax, 5.0, 6.5, 5.5, 4.7)
    
    # Denoising loop
    add_box(ax, 4.5, 2.0, 3, 0.6, 'Denoising (T steps)', '#ef6c00')
    add_arrow(ax, 6.0, 3.5, 6.0, 2.6)
    
    add_arrow(ax, 6.0, 2.0, 6.0, 1.3)
    add_box(ax, 4.5, 0.5, 3, 0.7, 'Latent z_0', '#2e7d32')
    
    add_arrow(ax, 7.5, 0.9, 8.5, 0.9)
    add_box(ax, 8.5, 0.3, 1.5, 1.0, 'VAE\nDecoder', '#6a1b9a', fontsize=9)
    add_arrow(ax, 10.0, 0.8, 10.5, 0.8)
    add_box(ax, 10.5, 0.3, 1.5, 1.0, 'Image', '#2e7d32')
    
    save_svg(fig, 'stable_diffusion')

# ============================================================================
# 11. DIFFUSION PROCESS
# ============================================================================
def draw_diffusion_process():
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    setup_ax(ax, 'Diffusion Forward & Reverse Process')
    
    # Forward
    ax.text(2.5, 5.5, 'Forward Process q(x_t | x_{t-1})', ha='center', va='center',
            fontsize=11, color='#4fc3f7', fontweight='bold')
    
    x_vals = [1.0, 3.0, 5.0, 7.0]
    labels = ['x_0\n(Data)', 'x_1', 'x_t', 'x_T\n(Pure Noise)']
    for i, (x, label) in enumerate(zip(x_vals, labels)):
        gray = 0.9 - i*0.25
        color = f'#{int(gray*255):02x}{int(gray*255):02x}{int(gray*255):02x}'
        add_box(ax, x, 3.5, 1.5, 1.2, label, color, text_color='#111' if i < 2 else '#fff')
        if i < 3:
            add_arrow(ax, x+1.5, 4.1, x+1.5, 4.1)
            ax.text(x+1.5, 4.5, f'+N(0,β)', ha='center', va='center', fontsize=8, color='#888')
    
    # Reverse
    ax.text(7.5, 2.5, 'Reverse Process p_θ(x_{t-1} | x_t)', ha='center', va='center',
            fontsize=11, color='#ff8a65', fontweight='bold')
    
    for i in range(4):
        x = 8.5 - i*1.8
        gray = 0.15 + i*0.25
        color = f'#{int(gray*255):02x}{int(gray*255):02x}{int(gray*255):02x}'
        add_box(ax, x, 0.5, 1.5, 1.2, '', color)
        if i < 3:
            add_arrow(ax, x, 1.1, x-0.3, 1.1)
            ax.text(x-0.9, 1.5, 'Denoise', ha='center', va='center', fontsize=8, color='#888')
    
    ax.text(8.2, 1.1, 'x_T', ha='center', va='center', fontsize=9, color='white')
    ax.text(6.4, 1.1, '...', ha='center', va='center', fontsize=9, color='white')
    ax.text(4.6, 1.1, 'x_1', ha='center', va='center', fontsize=9, color='#111')
    ax.text(2.8, 1.1, 'x_0', ha='center', va='center', fontsize=9, color='#111')
    
    save_svg(fig, 'diffusion_process')

# ============================================================================
# 12. RLHF PIPELINE
# ============================================================================
def draw_rlhf():
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    setup_ax(ax, 'RLHF: Reinforcement Learning from Human Feedback')
    
    # Stage 1: SFT
    add_box(ax, 0.5, 5.5, 2.5, 0.8, 'SFT Model\n(Supervised)', '#1565c0')
    add_arrow(ax, 1.75, 5.5, 1.75, 4.8)
    add_box(ax, 0.5, 4.0, 2.5, 0.7, 'Generate Responses', '#6a1b9a')
    
    # Human feedback
    add_arrow(ax, 3.0, 4.3, 4.0, 4.3)
    add_box(ax, 4.0, 3.8, 2.5, 0.8, 'Human Ranking\n(y_w > y_l)', '#ff8a65')
    add_arrow(ax, 5.25, 3.8, 5.25, 3.0)
    add_box(ax, 4.0, 2.2, 2.5, 0.7, 'Reward Model\nr_θ(x,y)', '#c62828')
    
    # PPO loop
    add_arrow(ax, 5.25, 2.2, 5.25, 1.5)
    add_box(ax, 4.0, 0.8, 2.5, 0.6, 'PPO Optimization', '#2e7d32')
    
    # KL penalty reference
    add_box(ax, 0.5, 0.8, 2.5, 0.6, 'SFT Policy\n(Reference)', '#455a64', fontsize=9)
    add_arrow(ax, 3.0, 1.1, 4.0, 1.1)
    ax.text(3.5, 1.4, 'KL', ha='center', va='center', fontsize=9, color='#888')
    
    # Output
    add_arrow(ax, 6.5, 1.1, 7.5, 1.1)
    add_box(ax, 7.5, 0.6, 2.5, 0.9, 'Aligned Policy\nπ_RL', '#2e7d32')
    
    save_svg(fig, 'rlhf')

# ============================================================================
# 13. RAG ARCHITECTURE
# ============================================================================
def draw_rag():
    fig, ax = plt.subplots(1, 1, figsize=(10, 7))
    setup_ax(ax, 'Retrieval-Augmented Generation (RAG)')
    
    # Query
    add_box(ax, 0.5, 5.5, 2, 0.7, 'User Query', '#1565c0')
    add_arrow(ax, 1.5, 5.5, 1.5, 4.8)
    
    # Retriever
    add_box(ax, 0.5, 4.0, 2, 0.7, 'Dense Retriever\n(Dual Encoder)', '#c62828')
    add_arrow(ax, 1.5, 4.0, 1.5, 3.3)
    
    # Knowledge base
    add_box(ax, 0.2, 2.0, 2.6, 1.0, 'Knowledge Base\n(Documents)', '#455a64', fontsize=9)
    add_arrow(ax, 2.8, 2.5, 3.5, 2.5)
    
    # Top-k docs
    add_box(ax, 3.5, 2.0, 2.5, 0.9, 'Top-k\nDocuments', '#6a1b9a')
    add_arrow(ax, 4.75, 2.9, 4.75, 3.5)
    
    # Generator
    add_box(ax, 3.5, 3.5, 2.5, 0.8, 'Generator\n(Seq2Seq LM)', '#2e7d32')
    
    # Concatenate
    add_arrow(ax, 2.5, 5.2, 3.5, 3.9)
    ax.text(2.8, 4.8, '+', ha='center', va='center', fontsize=14, color='#fff')
    
    add_arrow(ax, 4.75, 3.5, 4.75, 2.8)
    add_box(ax, 3.5, 1.8, 2.5, 0.8, 'Generated\nResponse', '#2e7d32')
    
    save_svg(fig, 'rag')

# ============================================================================
# 14. REACT AGENT
# ============================================================================
def draw_react():
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    setup_ax(ax, 'ReAct: Reasoning + Acting')
    
    steps = [
        (1.0, 4.5, 'Thought 1', '#6a1b9a'),
        (3.5, 4.5, 'Action 1', '#c62828'),
        (6.0, 4.5, 'Observation 1', '#1565c0'),
        (1.0, 2.5, 'Thought 2', '#6a1b9a'),
        (3.5, 2.5, 'Action 2', '#c62828'),
        (6.0, 2.5, 'Observation 2', '#1565c0'),
    ]
    
    for x, y, text, color in steps:
        add_box(ax, x, y, 2, 0.7, text, color)
    
    # Arrows
    add_arrow(ax, 3.0, 4.85, 3.5, 4.85)
    add_arrow(ax, 5.5, 4.85, 6.0, 4.85)
    add_arrow(ax, 7.0, 4.5, 7.5, 3.5)
    add_arrow(ax, 7.5, 3.5, 3.0, 2.85)
    add_arrow(ax, 3.0, 2.85, 3.5, 2.85)
    add_arrow(ax, 5.5, 2.85, 6.0, 2.85)
    add_arrow(ax, 7.0, 2.5, 7.5, 1.5)
    add_arrow(ax, 7.5, 1.5, 2.0, 1.5)
    
    add_box(ax, 0.5, 0.5, 2.5, 0.7, 'Final Answer', '#2e7d32')
    add_arrow(ax, 2.0, 1.5, 2.0, 1.2)
    
    save_svg(fig, 'react')

# ============================================================================
# 15. RESNET BLOCK
# ============================================================================
def draw_resnet():
    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    setup_ax(ax, 'ResNet: Residual Learning Block')
    
    # Main path
    add_box(ax, 0.5, 2.5, 1.5, 0.8, 'x', '#1565c0')
    add_arrow(ax, 2.0, 2.9, 2.5, 2.9)
    add_box(ax, 2.5, 2.5, 2, 0.8, 'Conv 3x3', '#c62828')
    add_arrow(ax, 4.5, 2.9, 5.0, 2.9)
    add_box(ax, 5.0, 2.5, 1.5, 0.8, 'BN', '#455a64')
    add_arrow(ax, 6.5, 2.9, 7.0, 2.9)
    add_box(ax, 7.0, 2.5, 1.5, 0.8, 'ReLU', '#ef6c00')
    add_arrow(ax, 8.5, 2.9, 9.0, 2.9)
    add_box(ax, 9.0, 2.5, 2, 0.8, 'Conv 3x3', '#c62828')
    add_arrow(ax, 11.0, 2.9, 11.5, 2.9)
    add_box(ax, 11.5, 2.5, 1.5, 0.8, 'BN', '#455a64')
    
    # Skip connection
    ax.annotate('', xy=(13.5, 2.9), xytext=(2.0, 2.9),
               arrowprops=dict(arrowstyle='->', color='#00d4aa', lw=2,
                              connectionstyle="arc3,rad=-0.3"))
    ax.text(7.5, 1.5, 'Skip Connection: F(x) + x', ha='center', va='center',
            fontsize=10, color='#00d4aa', fontweight='bold')
    
    # Final
    add_arrow(ax, 13.0, 2.5, 13.0, 1.8)
    add_box(ax, 12.0, 0.8, 2, 0.9, 'ReLU', '#ef6c00')
    
    save_svg(fig, 'resnet')

# ============================================================================
# 16. LSTM CELL
# ============================================================================
def draw_lstm():
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    setup_ax(ax, 'LSTM Cell (Hochreiter & Schmidhuber, 1997)')
    
    # Inputs
    add_box(ax, 0.3, 6.5, 1.5, 0.6, 'x_t', '#1565c0')
    add_box(ax, 0.3, 5.0, 1.5, 0.6, 'h_{t-1}', '#1565c0')
    add_box(ax, 0.3, 3.5, 1.5, 0.6, 'c_{t-1}', '#1565c0')
    
    # Gates
    gates = [
        (3.0, 6.5, 'Forget Gate\nf_t = σ(W_f·[h,x]+b)'),
        (3.0, 5.0, 'Input Gate\ni_t = σ(W_i·[h,x]+b)'),
        (3.0, 3.5, 'Candidate\nC_t = tanh(W_C·[h,x]+b)'),
        (3.0, 2.0, 'Output Gate\no_t = σ(W_o·[h,x]+b)'),
    ]
    for x, y, text in gates:
        add_box(ax, x, y, 3.5, 0.9, text, '#c62828', fontsize=8)
    
    # Cell state operations
    add_box(ax, 7.5, 5.0, 2, 0.8, 'x (element)', '#6a1b9a')
    add_box(ax, 7.5, 3.5, 2, 0.8, '+ (element)', '#6a1b9a')
    
    # Outputs
    add_box(ax, 10.5, 3.5, 1.5, 0.6, 'c_t', '#2e7d32')
    add_box(ax, 10.5, 2.0, 1.5, 0.6, 'h_t', '#2e7d32')
    
    # Arrows
    add_arrow(ax, 1.8, 6.8, 3.0, 6.8)
    add_arrow(ax, 1.8, 5.3, 3.0, 5.3)
    add_arrow(ax, 1.8, 3.8, 3.0, 3.8)
    
    add_arrow(ax, 6.5, 5.4, 7.5, 5.4)
    add_arrow(ax, 6.5, 3.9, 7.5, 3.9)
    add_arrow(ax, 6.5, 2.4, 7.5, 2.4)
    
    add_arrow(ax, 9.5, 5.0, 9.5, 3.8)
    add_arrow(ax, 9.5, 3.5, 10.5, 3.8)
    add_arrow(ax, 9.5, 3.5, 9.5, 2.3)
    add_arrow(ax, 9.5, 2.0, 10.5, 2.3)
    
    save_svg(fig, 'lstm')

# ============================================================================
# 17. CNN ARCHITECTURE
# ============================================================================
def draw_cnn():
    fig, ax = plt.subplots(1, 1, figsize=(12, 5))
    setup_ax(ax, 'CNN: Convolutional Neural Network (LeNet/AlexNet Style)')
    
    layers = [
        (0.5, 'Input\nImage', '#1565c0', 1.0),
        (2.0, 'Conv\n+ ReLU', '#c62828', 1.2),
        (3.7, 'Pool', '#455a64', 0.8),
        (5.0, 'Conv\n+ ReLU', '#c62828', 1.2),
        (6.7, 'Pool', '#455a64', 0.8),
        (8.0, 'Conv\n+ ReLU', '#c62828', 1.2),
        (9.7, 'Flatten', '#6a1b9a', 0.8),
        (11.0, 'FC', '#ef6c00', 1.0),
        (12.5, 'Output', '#2e7d32', 1.0),
    ]
    
    for i, (x, text, color, w) in enumerate(layers):
        add_box(ax, x, 2.0, w, 1.5, text, color, fontsize=9)
        if i < len(layers) - 1:
            add_arrow(ax, x+w, 2.75, layers[i+1][0], 2.75)
    
    save_svg(fig, 'cnn')

# ============================================================================
# 18. GAN
# ============================================================================
def draw_gan():
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    setup_ax(ax, 'GAN: Generative Adversarial Network')
    
    # Generator
    add_box(ax, 0.5, 4.5, 2.5, 0.8, 'Noise z ~ p(z)', '#1565c0')
    add_arrow(ax, 1.75, 4.5, 1.75, 3.8)
    add_box(ax, 0.5, 3.0, 2.5, 0.7, 'Generator G', '#c62828')
    add_arrow(ax, 1.75, 3.0, 1.75, 2.3)
    add_box(ax, 0.5, 1.5, 2.5, 0.7, 'Fake Data G(z)', '#6a1b9a')
    
    # Discriminator
    add_box(ax, 7.0, 5.5, 2.5, 0.6, 'Real Data x', '#1565c0')
    add_arrow(ax, 8.25, 5.5, 8.25, 4.3)
    
    add_arrow(ax, 3.0, 1.8, 7.0, 3.0)
    add_box(ax, 7.0, 2.5, 2.5, 1.0, 'Discriminator D', '#c62828')
    add_arrow(ax, 8.25, 2.5, 8.25, 1.5)
    add_box(ax, 7.0, 0.5, 2.5, 0.9, 'Real / Fake', '#2e7d32')
    
    # Feedback loops
    ax.annotate('', xy=(3.0, 3.3), xytext=(7.0, 3.3),
               arrowprops=dict(arrowstyle='->', color='#ff8a65', lw=1.5,
                              connectionstyle="arc3,rad=0.2"))
    ax.text(5.0, 4.0, 'Train D', ha='center', va='center', fontsize=9, color='#ff8a65')
    
    ax.annotate('', xy=(3.0, 2.7), xytext=(7.0, 2.7),
               arrowprops=dict(arrowstyle='->', color='#00d4aa', lw=1.5,
                              connectionstyle="arc3,rad=-0.2"))
    ax.text(5.0, 1.8, 'Train G', ha='center', va='center', fontsize=9, color='#00d4aa')
    
    save_svg(fig, 'gan')

# ============================================================================
# 19. VAE
# ============================================================================
def draw_vae():
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    setup_ax(ax, 'VAE: Variational Autoencoder')
    
    # Encoder
    add_box(ax, 0.5, 4.5, 2, 0.7, 'Input x', '#1565c0')
    add_arrow(ax, 1.5, 4.5, 1.5, 3.8)
    add_box(ax, 0.5, 3.0, 2, 0.7, 'Encoder', '#c62828')
    add_arrow(ax, 1.5, 3.0, 1.5, 2.3)
    
    # Latent
    add_box(ax, 0.3, 1.5, 1.2, 0.6, 'μ', '#6a1b9a', fontsize=10)
    add_box(ax, 1.7, 1.5, 1.2, 0.6, 'σ', '#6a1b9a', fontsize=10)
    add_arrow(ax, 1.5, 1.5, 1.5, 0.8)
    add_box(ax, 0.5, 0.2, 2, 0.5, 'z = μ + σ⊙ε', '#6a1b9a', fontsize=9)
    
    # Decoder
    add_arrow(ax, 2.5, 0.45, 3.5, 0.45)
    add_box(ax, 3.5, 3.0, 2, 0.7, 'Decoder', '#c62828')
    add_arrow(ax, 3.5, 0.45, 4.0, 2.3)
    add_arrow(ax, 4.5, 3.0, 4.5, 2.3)
    add_box(ax, 3.5, 1.5, 2, 0.7, 'Reconstruct x̂', '#2e7d32')
    
    # Loss
    add_arrow(ax, 5.5, 1.85, 6.5, 1.85)
    add_box(ax, 6.5, 1.3, 2.5, 0.9, 'Reconstruction\n+ KL Divergence', '#ff8a65', fontsize=9)
    
    save_svg(fig, 'vae')

# ============================================================================
# 20. STATE SPACE MODEL (MAMBA)
# ============================================================================
def draw_mamba():
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    setup_ax(ax, 'Mamba: Selective State Space Model')
    
    add_box(ax, 0.5, 4.5, 2, 0.7, 'Input x_t', '#1565c0')
    add_arrow(ax, 1.5, 4.5, 1.5, 3.8)
    
    # Linear projections
    add_box(ax, 0.5, 3.0, 2, 0.7, 'Linear', '#455a64')
    add_arrow(ax, 1.5, 3.0, 1.5, 2.3)
    
    # Selection
    add_box(ax, 0.3, 1.5, 1.0, 0.6, 'Δ_t', '#c62828', fontsize=10)
    add_box(ax, 1.5, 1.5, 1.0, 0.6, 'B_t', '#c62828', fontsize=10)
    add_box(ax, 2.7, 1.5, 1.0, 0.6, 'C_t', '#c62828', fontsize=10)
    ax.text(1.5, 2.2, 'Input-dependent parameters', ha='center', va='center', 
            fontsize=9, color='#ff8a65')
    
    # SSM core
    add_arrow(ax, 2.0, 1.5, 4.0, 1.8)
    add_box(ax, 4.0, 1.3, 2.5, 0.9, 'SSM Core\nh_t = Ā h_{t-1} + B̄ x_t', '#6a1b9a', fontsize=9)
    add_arrow(ax, 5.25, 1.3, 5.25, 0.6)
    
    # Output
    add_box(ax, 4.0, -0.1, 2.5, 0.6, 'y_t = C h_t', '#2e7d32')
    
    # Skip
    add_arrow(ax, 2.5, 4.8, 5.0, 4.8)
    add_arrow(ax, 5.0, 4.8, 5.0, 0.3)
    add_box(ax, 5.0, -0.1, 1.5, 0.6, '+', '#455a64', fontsize=14)
    add_arrow(ax, 6.5, 0.2, 7.5, 0.2)
    add_box(ax, 7.5, -0.3, 2, 0.9, 'Output y_t', '#2e7d32')
    
    save_svg(fig, 'mamba')

# ============================================================================
# 21. LLaMA ARCHITECTURE
# ============================================================================
def draw_llama():
    fig, ax = plt.subplots(1, 1, figsize=(8, 10))
    setup_ax(ax, 'LLaMA Architecture')
    
    add_box(ax, 1.5, 8.5, 7, 0.7, 'Input Tokens', '#1565c0')
    add_box(ax, 1.5, 7.6, 7, 0.6, 'Token Embedding', '#455a64', fontsize=9)
    add_box(ax, 1.5, 6.8, 7, 0.6, 'RMSNorm', '#455a64', fontsize=9)
    
    for i in range(3):
        y = 5.8 - i*1.6
        add_box(ax, 1.5, y+0.5, 7, 0.6, 'Grouped Query Attention + RoPE', '#c62828', fontsize=9)
        add_box(ax, 4.2, y+0.05, 1.6, 0.3, 'RMSNorm', '#455a64', fontsize=8)
        add_box(ax, 1.5, y-0.5, 7, 0.6, 'SwiGLU FFN', '#ef6c00')
        add_box(ax, 4.2, y-0.95, 1.6, 0.3, 'RMSNorm', '#455a64', fontsize=8)
        if i < 2:
            ax.annotate('', xy=(5, y-0.95), xytext=(5, y+0.5+0.7),
                       arrowprops=dict(arrowstyle='->', color='#888', lw=1))
    
    ax.text(5, 4.0, 'x32-80 layers', ha='center', va='center', fontsize=10, color='#888', style='italic')
    
    add_box(ax, 1.5, 0.5, 7, 0.7, 'RMSNorm + LM Head', '#2e7d32')
    add_arrow(ax, 5, 1.2, 5, 1.8)
    add_box(ax, 1.5, -0.4, 7, 0.7, 'Next Token Distribution', '#2e7d32')
    
    save_svg(fig, 'llama')

# ============================================================================
# 22. TEST-TIME COMPUTE (o1)
# ============================================================================
def draw_test_time_compute():
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    setup_ax(ax, 'Test-Time Compute Scaling (o1 / o3)')
    
    # Traditional
    add_box(ax, 0.5, 5.0, 3, 0.7, 'Prompt', '#1565c0')
    add_arrow(ax, 2.0, 5.0, 2.0, 4.3)
    add_box(ax, 0.5, 3.5, 3, 0.7, 'Base LLM', '#c62828')
    add_arrow(ax, 2.0, 3.5, 2.0, 2.8)
    add_box(ax, 0.5, 2.0, 3, 0.7, 'Answer', '#2e7d32')
    ax.text(2.0, 1.2, 'Traditional: Scale Model', ha='center', va='center', 
            fontsize=10, color='#888')
    
    # Test-time compute
    add_box(ax, 5.5, 5.0, 3, 0.7, 'Prompt', '#1565c0')
    add_arrow(ax, 7.0, 5.0, 7.0, 4.3)
    add_box(ax, 5.5, 3.5, 3, 0.7, 'Reasoning Model', '#c62828')
    add_arrow(ax, 7.0, 3.5, 7.0, 2.8)
    add_box(ax, 5.5, 2.0, 3, 0.7, 'Chain-of-Thought', '#6a1b9a')
    add_arrow(ax, 7.0, 2.0, 7.0, 1.3)
    add_box(ax, 5.5, 0.5, 3, 0.7, 'Verify / Revise', '#ef6c00')
    add_arrow(ax, 7.0, 0.5, 7.0, -0.2)
    add_box(ax, 5.5, -1.0, 3, 0.7, 'Final Answer', '#2e7d32')
    
    # Loop back
    ax.annotate('', xy=(8.5, 1.5), xytext=(8.5, 0.8),
               arrowprops=dict(arrowstyle='->', color='#ff8a65', lw=1.5,
                              connectionstyle="arc3,rad=0.3"))
    ax.text(9.3, 1.2, 'Iterate', ha='center', va='center', fontsize=9, color='#ff8a65')
    
    ax.text(7.0, -1.8, 'New: Scale Thinking Time', ha='center', va='center', 
            fontsize=10, color='#888')
    
    save_svg(fig, 'test_time_compute')

# ============================================================================
# 23. DPO (Direct Preference Optimization)
# ============================================================================
def draw_dpo():
    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    setup_ax(ax, 'DPO: Direct Preference Optimization')
    
    add_box(ax, 0.5, 3.5, 2.5, 0.7, 'Prompt x', '#1565c0')
    
    add_arrow(ax, 1.75, 3.5, 1.75, 2.8)
    add_box(ax, 0.5, 2.0, 2.5, 0.7, 'Policy π_θ', '#c62828')
    
    add_arrow(ax, 3.0, 2.35, 3.5, 2.35)
    add_box(ax, 3.5, 2.0, 2, 0.7, 'y_w (win)', '#2e7d32')
    add_arrow(ax, 3.0, 2.05, 3.5, 1.25)
    add_box(ax, 3.5, 0.5, 2, 0.7, 'y_l (lose)', '#ff8a65')
    
    add_box(ax, 6.0, 1.25, 2.5, 1.0, 'Log Ratio\nlog[π(y_w)/π_ref(y_w)]\n- log[π(y_l)/π_ref(y_l)]', '#6a1b9a', fontsize=8)
    add_arrow(ax, 5.5, 2.35, 6.0, 1.75)
    add_arrow(ax, 5.5, 0.85, 6.0, 1.25)
    
    add_arrow(ax, 8.5, 1.75, 9.0, 1.75)
    add_box(ax, 9.0, 1.25, 2, 0.9, 'Maximize\nPreference', '#2e7d32')
    
    save_svg(fig, 'dpo')

# ============================================================================
# 24. WHISPER
# ============================================================================
def draw_whisper():
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    setup_ax(ax, 'Whisper: Robust Speech Recognition')
    
    add_box(ax, 0.5, 4.5, 2.5, 0.7, 'Audio', '#1565c0')
    add_arrow(ax, 1.75, 4.5, 1.75, 3.8)
    add_box(ax, 0.5, 3.0, 2.5, 0.7, 'Log-Mel\nSpectrogram', '#6a1b9a')
    add_arrow(ax, 1.75, 3.0, 1.75, 2.3)
    add_box(ax, 0.5, 1.5, 2.5, 0.7, 'Encoder\n(Transformer)', '#c62828')
    
    add_arrow(ax, 3.0, 1.85, 3.5, 1.85)
    add_box(ax, 3.5, 1.5, 2.5, 0.7, 'Cross-Attention', '#ff8a65')
    
    add_box(ax, 3.5, 3.5, 2.5, 0.7, 'Decoder\n(Transformer)', '#c62828')
    add_arrow(ax, 4.75, 3.5, 4.75, 2.2)
    
    add_arrow(ax, 6.0, 1.85, 6.5, 1.85)
    add_box(ax, 6.5, 1.5, 2.5, 0.7, 'Text Tokens', '#2e7d32')
    
    # Special tokens
    add_box(ax, 6.8, 3.8, 2.2, 0.5, '<|transcribe|>', '#455a64', fontsize=8)
    add_box(ax, 6.8, 3.2, 2.2, 0.5, '<|translate|>', '#455a64', fontsize=8)
    add_arrow(ax, 7.9, 3.8, 7.9, 3.5)
    add_arrow(ax, 7.9, 3.2, 7.9, 3.5)
    
    save_svg(fig, 'whisper')

# ============================================================================
# 25. AGENT LOOP
# ============================================================================
def draw_agent_loop():
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    setup_ax(ax, 'Agent Architecture Loop')
    
    # Center
    add_box(ax, 3.0, 3.5, 4, 1.2, 'LLM (Brain)', '#c62828')
    
    # Perception
    add_box(ax, 0.5, 5.5, 2.5, 0.8, 'Perception', '#1565c0')
    add_arrow(ax, 3.0, 5.9, 1.75, 5.9)
    add_arrow(ax, 1.75, 5.5, 3.0, 4.7)
    
    # Memory
    add_box(ax, 7.0, 5.5, 2.5, 0.8, 'Memory', '#6a1b9a')
    add_arrow(ax, 7.0, 5.9, 5.0, 5.9)
    add_arrow(ax, 5.0, 5.5, 5.0, 4.7)
    
    # Planning
    add_box(ax, 0.5, 1.5, 2.5, 0.8, 'Planning', '#ff8a65')
    add_arrow(ax, 3.0, 3.5, 1.75, 3.1)
    add_arrow(ax, 1.75, 2.3, 3.0, 2.3)
    
    # Action/Tools
    add_box(ax, 7.0, 1.5, 2.5, 0.8, 'Tools/Action', '#2e7d32')
    add_arrow(ax, 5.0, 3.5, 6.5, 3.1)
    add_arrow(ax, 6.5, 2.3, 5.0, 2.3)
    
    # Environment
    add_box(ax, 3.0, 0.2, 4, 0.8, 'Environment', '#455a64')
    add_arrow(ax, 4.0, 1.5, 4.0, 1.0)
    add_arrow(ax, 5.0, 1.0, 5.0, 1.5)
    
    save_svg(fig, 'agent_loop')

if __name__ == '__main__':
    draw_transformer()
    draw_self_attention()
    draw_multihead_attention()
    draw_bert()
    draw_gpt()
    draw_t5()
    draw_moe()
    draw_vit()
    draw_clip()
    draw_stable_diffusion()
    draw_diffusion_process()
    draw_rlhf()
    draw_rag()
    draw_react()
    draw_resnet()
    draw_lstm()
    draw_cnn()
    draw_gan()
    draw_vae()
    draw_mamba()
    draw_llama()
    draw_test_time_compute()
    draw_dpo()
    draw_whisper()
    draw_agent_loop()
    print("All diagrams generated!")
