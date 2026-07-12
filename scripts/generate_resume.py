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
    # 注意：反斜杠必须最先替换，否则新增的 \ 也会被转义
    replacements = [
        ('\\', r'\textbackslash{}'),  # 必须第一个
        ('&', r'\&'),
        ('%', r'\%'),
        ('$', r'\$'),
        ('#', r'\#'),
        ('_', r'\_'),
        ('{', r'\{'),
        ('}', r'\}'),
        ('~', r'\textasciitilde{}'),
        ('^', r'\^{}'),
    ]
    for old, new in replacements:
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
    
    # 获取开关选项
    options = data.get('options', {})
    has_work = options.get('hasWorkExperience', True)
    auto_one_page = options.get('autoOnePage', True)
    
    # 弹性间距（仅 autoOnePage 开启时）
    if auto_one_page:
        latex_lines.append('\\vfill')
    
    # 工作经历 / 过往经历（根据开关切换）
    if has_work:
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
                # 支持两种结构：project_groups（分组）或 projects（平铺）
                project_groups = exp.get('project_groups', [])
                projects = exp.get('projects', [])
                
                if project_groups or projects:
                    latex_lines.append('\\begin{onehalfspacing}')
                    
                    # 分组结构（如：稳定性相关工作、监控与可观测相关工作）
                    if project_groups:
                        for group in project_groups:
                            group_title = group.get('group_title', '')
                            group_icon = group.get('group_icon', 'faShield')
                            group_projects = group.get('projects', [])
                            
                            if group_title:
                                latex_lines.append(
                                    f'\\subsection{{\\Large \\{group_icon}\\ \\textbf{{{escape_latex(group_title)}}}}}'
                                )
                            
                            for proj in group_projects:
                                title = proj.get('title', '')
                                icon = proj.get('icon', group_icon)
                                challenge = proj.get('challenge', '')
                                achievements = proj.get('achievements', [])
                                
                                latex_lines.append(
                                    f'\\subsection{{\\textbf{{\\$\\blacktriangleright\\$}} {escape_latex(title)}}}'
                                )
                                
                                if challenge:
                                    latex_lines.append(f'\\textbf{{挑战：}} {escape_latex(challenge)}')
                                
                                if achievements:
                                    latex_lines.append('\\begin{itemize}')
                                    for ach in achievements:
                                        latex_lines.append(f'  \\item {escape_latex(ach)}')
                                    latex_lines.append('\\end{itemize}')
                    
                    # 平铺结构（兼容旧格式）
                    elif projects:
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
    else:
        # 过往经历（应届生）
        past_experiences = data.get('past_experience', [])
        if past_experiences:
            latex_lines.append('\\section{\\faHistory\\ 过往经历}')
            
            for pe in past_experiences:
                name = pe.get('name', '')
                period = pe.get('period', '')
                role = pe.get('role', '')
                tech = pe.get('tech', '')
                description = pe.get('description', '')
                achievements_str = pe.get('achievements', '')
                
                title = f'{escape_latex(name)}（{escape_latex(period)}）' if period else escape_latex(name)
                latex_lines.append(f'\\subsection{{\\textbf{{{title}}}}}')
                
                meta = ' | '.join(filter(None, [role, tech]))
                if meta:
                    latex_lines.append(f'\\textit{{{escape_latex(meta)}}}')
                
                if description:
                    latex_lines.append(escape_latex(description))
                
                if achievements_str:
                    achievements = [a.strip() for a in achievements_str.split('\n') if a.strip()]
                    if achievements:
                        latex_lines.append('\\begin{itemize}')
                        for ach in achievements:
                            latex_lines.append(f'  \\item {escape_latex(ach)}')
                        latex_lines.append('\\end{itemize}')
                
                latex_lines.append('')
    
    if auto_one_page:
        latex_lines.append('\vfill')  # 弹性间距
    
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