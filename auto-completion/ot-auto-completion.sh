#!/usr/bin/env sh

ABS_PATH='absolute path here'

_ot_completions()
{
  keys=$(/usr/bin/env python3 $ABS_PATH/ot-auto-completion.py ${COMP_WORDS[@]:0:$COMP_CWORD})
  COMPREPLY=($(compgen -W "$keys" "${COMP_WORDS[$COMP_CWORD]}"))
}

complete -F _ot_completions ./ot.py
