#!/usr/bin/env sh
_ot_completions()
{
  keys=$(/usr/bin/env python3 /<absolutepath>/ot-auto-complete.py ${COMP_WORDS[@]:0:$COMP_CWORD})
  COMPREPLY=($(compgen -W "$keys" "${COMP_WORDS[$COMP_CWORD]}"))
}

complete -F _ot_completions ./ot.py
