#!/usr/bin/env sh

_ot_completions()
{
  keys=$(/usr/bin/env oi completion ${COMP_WORDS[@]:0:$COMP_CWORD})
  COMPREPLY=($(compgen -W "$keys" "${COMP_WORDS[$COMP_CWORD]}"))
}

complete -F _ot_completions oi