#!/usr/bin/env python

import os
import errno
import shutil
import subprocess
import sys

import matplotlib
matplotlib.rcParams.update({
    'text.usetex': True,
    'text.latex.preamble': [r'\usepackage{siunitx}', r'\sisetup{per-mode=symbol}', \
        r'\DeclareSIUnit[number-unit-product = \text{ }]\bjd{BJD}', r'\DeclareSIUnit\electron{\ensuremath{\mathrm{e^-}}}' \
        r'\DeclareSIUnit[number-unit-product = \text{ }]\solarRadius{R_{\astrosun}}', r'\DeclareSIUnit[number-unit-product = \text{ }]\jupiterRadius{R_J}'],
    'font.family': 'serif'
})

documents_dir = os.path.realpath(os.path.dirname(__file__))
root_dir = os.path.normpath(os.path.join(documents_dir, '..'))

build_dir = os.path.join(root_dir, 'build')
gen_dir = os.path.join(build_dir, 'gen')

sys.path.append(root_dir)

from exo.documents import *

try:
    shutil.rmtree(build_dir)
except OSError as e:
    pass
mkdir_p(build_dir)
mkdir_p(gen_dir)

context = make(gen_dir)
# jinja_env = create_latex_env([documents_dir])
#
# environment = {
#     'PATH': os.environ.get('PATH', os.defpath),
#     'TEXINPUTS': os.pathsep.join(['.', documents_dir, os.environ.get('TEXINPUTS', '')]),
#     'BIBINPUTS': os.pathsep.join(['.', documents_dir, os.environ.get('BIBINPUTS', '')])
# }
#
# mkdir_p(os.path.join(build_dir, 'report'))
# mkdir_p(os.path.join(build_dir, 'presentation'))
#
# with open(os.path.join(build_dir, 'report', 'report.tex'), 'w') as out:
#     out.write(jinja_env.get_template('report/report.tex').render(context))
# with open(os.path.join(build_dir, 'presentation', 'presentation.tex'), 'w') as out:
#     out.write(jinja_env.get_template('presentation/presentation.beamer.tex').render(context))
# with open(os.path.join(build_dir, 'presentation', 'notes.tex'), 'w') as out:
#     out.write(jinja_env.get_template('presentation/presentation.notes.tex').render(context))
#
# for document, dir in {'report': 'report', 'notes': 'presentation', 'presentation': 'presentation'}.iteritems():
#     subprocess.check_call(["xelatex", document], cwd=dir, env=environment)
#     subprocess.check_call(["biber", document], cwd=dir, env=environment)
#     subprocess.check_call(["xelatex", document], cwd=dir, env=environment)

def process(document, biber=True):
    input_dir = os.path.join(documents_dir, document)
    jinja_env = create_latex_env([documents_dir, input_dir])
    template = jinja_env.get_template('{0}/{0}.tex'.format(document))
    # template = jinja_env.get_template(document + '.tex')
    output_dir = os.path.join(build_dir, os.path.basename(document))
    mkdir_p(output_dir)
    with open(os.path.join(output_dir, document + '.tex'), 'w') as generated_document:
        generated_document.write(template.render(context))

    environment = {
        'PATH': os.environ.get('PATH', os.defpath),
        'TEXINPUTS': '.' + os.pathsep + input_dir + os.pathsep + documents_dir + os.pathsep + os.environ.get('TEXINPUTS', ''),
        'BIBINPUTS': '.' + os.pathsep + documents_dir + os.pathsep + os.environ.get('BIBINPUTS', '')
    }

    subprocess.check_call(["xelatex", document], cwd=output_dir, env=environment)
    if biber:
        subprocess.check_call(["biber", document], cwd=output_dir, env=environment)
        subprocess.check_call(["xelatex", document], cwd=output_dir, env=environment)

# subprocess.check_call(["pdfnup", "--no-landscape", "--nup", "1x2", "--scale", "0.9", "--twoside", "--offset", "0.8cm 0cm", os.path.join(build_dir, "notes", "notes.pdf")])

process('report')
process('beamer')
process('notes', biber=False)
