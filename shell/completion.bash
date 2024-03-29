# pyviewer completion setting for bash

_pyviewer_cmp()
{
    local cur prev
    cur=${COMP_WORDS[${COMP_CWORD}]}
    prev=${COMP_WORDS[${COMP_CWORD}-1]}

    local opts="-h -t -iv -o -p -v -k -i -c --encoding"
    local types="$(_get_pyviewer_types 'type')"
    local image_viewer="$(_get_pyviewer_types 'image_viewer')"
    if [[ "${cur:0:1}" = "-" ]]; then
        COMPREPLY=( $(compgen -W "$opts" -- "$cur") )
    elif [[ "${prev}" = "-h" ]]; then
        # show help
        COMPREPLY=()
    elif [[ "${prev}" = "-t" ]]; then
        # select type
        COMPREPLY=( $(compgen -W "$types" -- "$cur") )
    elif [[ "${prev}" = "-iv" ]]; then
        # select image viewer
        COMPREPLY=( $(compgen -W "$image_viewer" -- "$cur") )
    else
        # select file
        compopt -o filenames
        COMPREPLY=( $(compgen -f -- "$cur") )
        COMPREPLY+=( $(compgen -W "update" -- "$cur") )
        COMPREPLY+=( $(compgen -W "config_list" -- "$cur") )
        COMPREPLY+=( $(compgen -W "help" -- "$cur") )
    fi
}

complete -F _pyviewer_cmp pyviewer
