#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简历生成器：从 JSON 数据生成 LaTeX 简历文件
"""

import json
import os
import argparse
from pathlib import Path
from datetime import datetime


def escape_latex(text: str) -> str:
    """转义 LaTeX 特殊字符"""
    replacements = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def generate_resume_latex(data: dict, template_dir: str = "resume") -> str:
    """
    根据简历数据生成 LaTeX 内容
    
    Args:
        data: 简历数据字典
        template_dir: 模板目录路径
        
    Returns:
        LaTeX 文档内容
    """
    latex_lines = []
    
    # 文档头部
    latex_lines.extend([
        '% !TEX TS-program = xelatex',
        '% !TEX encoding = UTF-8 Unicode',
        '% !Mode:: "TeX:UTF-8"',
        '',
        '\\documentclass{resume}',
        '\\usepackage{zh_CN-Adobefonts_external}',
        '\\usepackage{amssymb}',
        '\\usepackage{linespacing_fix}',
        '\\usepackage{cite}',
        '\\usepackage{fontawesome}',
        '\\begin{document}',
        '\\pagenumbering{gobble}',
        '',
    ])
    
    # 个人信息部分
    personal = data.get('personal', {})
    name = personal.get('name', '姓名')
    email = personal.get('email', '')
    phone = personal.get('phone', '')
    
    # 左侧：姓名和联系方式
    latex_lines.extend([
        '\\begin{minipage}{0.38\\textwidth}',
        '  \\centering',
        f'  \\Huge\\textbf{{{escape_latex(name)}}}',
        '',
        '  \\vspace{0.5em}',
        '',
        '  \\normalsize',
        '  \\basicInfo{',
        '    \\begin{tabular}[t]{@{}l@{}}',
        f'      \\email{{{escape_latex(email)}}} \\\\',
        f'      \\phone{{{escape_latex(phone)}}}',
        '    \\end{tabular}',
        '  }',
        '\\end{minipage}%',
    ])
    
    # 右侧：教育背景
    latex_lines.extend([
        '\\begin{minipage}{0.62\\textwidth}',
        '  \\raggedright',
        '  \\section{\\faGraduationCap\\ 教育背景}',
    ])
    
    education = data.get('education', [])
    for edu in education:
        school = edu.get('school', '')
        location = edu.get('location', '')
        period = edu.get('period', '')
        degree = edu.get('degree', '')
        major = edu.get('major', '')
        
        latex_lines.append(
            f'  \\datedsubsection{{\\textbf{{{escape_latex(school)}}}, {escape_latex(location)}}}{{{period}}}'
        )
        latex_lines.append(f'  \\textit{{{degree}}}\\ {escape_latex(major)}')
    
    latex_lines.append('\\end{minipage}')
    latex_lines.append('')
    
    # 工作经历
    experiences = data.get('experience', [])
    if experiences:
        latex_lines.append('\\section{\\Large \\faUsers\\ 工作经历}')
        
        for exp in experiences:
            company = exp.get('company', '')
            department = exp.get('department', '')
            period = exp.get('period', '')
            role = exp.get('role', '')
            responsibilities = exp.get('responsibilities', '')
            projects = exp.get('projects', [])
            
            # 公司和部门
            latex_lines.append(
                f'\\datedsubsection{{\\textbf{{{escape_latex(company)}}} \\space {{{escape_latex(department)}}}}}{{{period}}}'
            )
            latex_lines.append(f' \\role{{{escape_latex(role)}}}{{}}')
            latex_lines.append('')
            latex_lines.append('\\vspace{5pt}')
            latex_lines.append('')
            
            # 核心职责
            if responsibilities:
                latex_lines.append(
                    f'\\subsection{{\\Large \\faBullseye\\ \\textbf{{核心职责}}}}'
                )
                latex_lines.append(escape_latex(responsibilities))
                latex_lines.append('\\vspace{5pt}')
            
            # 项目/工作详情
            if projects:
                latex_lines.append('\\begin{onehalfspacing}')
                
                for proj in projects:
                    title = proj.get('title', '')
                    icon = proj.get('icon', 'faShield')
                    challenge = proj.get('challenge', '')
                    achievements = proj.get('achievements', [])
                    
                    latex_lines.append(
                        f'\\subsection{{\\large \\{icon}\\ \\textbf{{{escape_latex(title)}}}}}'
                    )
                    
                    if challenge:
                        latex_lines.append(f'\\textbf{{挑战：}} {escape_latex(challenge)}')
                    
                    if achievements:
                        latex_lines.append('\\begin{itemize}')
                        for ach in achievements:
                            latex_lines.append(f'  \\item {escape_latex(ach)}')
                        latex_lines.append('\\end{itemize}')
                
                latex_lines.append('\\end{onehalfspacing}')
            
            latex_lines.append('')
    
    # 技能
    skills = data.get('skills', [])
    if skills:
        latex_lines.append('\\section{\\faCogs\\ 技能}')
        latex_lines.append('\\begin{itemize}[parsep=0.5ex]')
        for skill in skills:
            latex_lines.append(f'  \\item {escape_latex(skill)}')
        latex_lines.append('\\end{itemize}')
        latex_lines.append('')
    
    # 文档结尾
    latex_lines.extend([
        '%% Reference',
        '%\\newpage',
        '%\\bibliographystyle{IEEETran}',
        '%\\bibliography{mycite}',
        '\\end{document}',
    ])
    
    return '\n'.join(latex_lines)


def create_resume_from_json(json_file: str, output_dir: str = "output", template_dir: str = "resume") -> str:
    """
    从 JSON 文件生成简历
    
    Args:
        json_file: JSON 数据文件路径
        output_dir: 输出目录
        template_dir: LaTeX 模板目录路径
        
    Returns:
        生成的 .tex 文件路径
    """
    # 读取 JSON 数据
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 生成 LaTeX 内容
    latex_content = generate_resume_latex(data, template_dir)
    
    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 生成输出文件名
    name = data.get('personal', {}).get('name', 'resume')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    tex_file = output_path / f'resume_{name}_{timestamp}.tex'
    
    # 写入文件
    with open(tex_file, 'w', encoding='utf-8') as f:
        f.write(latex_content)
    
    return str(tex_file)


def main():
    parser = argparse.ArgumentParser(description='从 JSON 数据生成 LaTeX 简历')
    parser.add_argument('json_file', help='简历 JSON 数据文件')
    parser.add_argument('--output-dir', '-o', default='output', help='输出目录（默认：output）')
    parser.add_argument('--template-dir', '-t', default='resume', help='LaTeX 模板目录（默认：resume）')
    
    args = parser.parse_args()
    
    tex_file = create_resume_from_json(args.json_file, args.output_dir, args.template_dir)
    print(f'✅ 简历已生成：{tex_file}')


if __name__ == '__main__':
    main()