```txt
                                                                                                                        
 Usage: makejinja [OPTIONS]                                                                                             
                                                                                                                        
 makejinja can be used to automatically generate files from Jinja templates.                                            
 Instead of passing CLI options, you can also write them to a file called makejinja.toml in your working directory.     
 Note: In this file, options may be named differently. Please refer to the file makejinja/config.py to see their actual 
 names. You will also find an example here: makejinja/tests/data/makejinja.toml.                                        
                                                                                                                        
╭─ Input/Output ───────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --input                DIRECTORY  Path to a folder containing template files. It is passed to Jinja's             │
│                                      FileSystemLoader when creating the environment. Note: This option may be passed │
│                                      multiple times to pass a list of values. If a template exists in multiple       │
│                                      inputs, the last value with be used.                                            │
│                                      [required]                                                                      │
│ *  --output               DIRECTORY  Path to a folder where the rendered templates are stored. makejinja preserves   │
│                                      the relative paths in the process, meaning that you can even use it on nested   │
│                                      directories.                                                                    │
│                                      [required]                                                                      │
│    --include-pattern      TEXT       Glob patterns to search for files in inputs. Accepts all pattern supported by   │
│                                      fnmatch. If a file is matched by this pattern and does not end with the         │
│                                      specified jinja-suffix, it is copied over to the output_folder. Multiple can be │
│                                      provided. Note: Do not add a special suffix used by your template files here,   │
│                                      instead use the jinja-suffix option.                                            │
│                                      [default: **/*]                                                                 │
│    --exclude-pattern      TEXT       Glob patterns pattern to exclude files matched. Applied against files           │
│                                      discovered through include_patterns. Multiple can be provided.                  │
│    --jinja-suffix         TEXT       File ending of Jinja template files. All files with this suffix in inputs       │
│                                      matched by pattern are passed to the Jinja renderer. Note: Should be provided   │
│                                      with the leading dot.                                                           │
│                                      [default: .jinja]                                                               │
│    --keep-jinja-suffix               Decide whether the specified jinja-suffix is removed from the file after        │
│                                      rendering.                                                                      │
│    --keep-empty                      Some Jinja template files may be empty after rendering (e.g., if they only      │
│                                      contain macros that are imported by other templates). By default, we do not     │
│                                      copy such empty files. If there is a need to have them available anyway, you    │
│                                      can adjust that.                                                                │
│    --copy-metadata                   Copy the file metadata (e.g., created/modified/permissions) from the input file │
│                                      using shutil.copystat                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Jinja Environment ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --data           PATH       Load variables from yaml/yml/toml/json files for use in your Jinja templates. The        │
│                             defintions are passed to Jinja's render function. Can either be a file or a folder       │
│                             containg files. Note: This option may be passed multiple times to pass a list of values. │
│                             If multiple files are supplied, beware that previous declarations will be overwritten by │
│                             newer ones.                                                                              │
│ --loader         TEXT       Use custom Python code to adjust the used Jinja environment to your needs. The specified │
│                             Python file should export a class containing a subset of the following functions:        │
│                             filters, globals, data, and extensions. In addition, you may add an __init__ function    │
│                             that recives two positional arguments: the created Jinja environment and the data parsed │
│                             from the files supplied to makejinja's data option. This allows you to apply aribtrary   │
│                             logic to makejinja. An import path can be specified either in dotted notation            │
│                             (your.custom.Loader) or with a colon as object delimiter (your.custom:Loader). Note:     │
│                             This option may be passed multiple times to pass a list of values.                       │
│ --import-path    DIRECTORY  In order to load custom loaders or Jinja extensions, the PYTHONPATH variable needs to be │
│                             patched. By default, makejinja will look for modules in your current directory, but you  │
│                             may change that.                                                                         │
│                             [default: .]                                                                             │
│ --extension      TEXT       List of Jinja extensions to use as strings of import paths. An overview of the built-in  │
│                             ones can be found on the project website. Note: This option may be passed multiple times │
│                             to pass a list of values.                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Jinja Whitespace ───────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --lstrip-blocks/--no-lstrip-blocks          If this is set to True, leading spaces and tabs are stripped from the    │
│                                             start of a line to a block.                                              │
│                                             [default: lstrip-blocks]                                                 │
│ --trim-blocks/--no-trim-blocks              If this is set to True, the first newline after a block is removed       │
│                                             (block, not variable tag!).                                              │
│                                             [default: trim-blocks]                                                   │
│ --keep-trailing-newline                     Preserve the trailing newline when rendering templates. The default is   │
│                                             False, which causes a single newline, if present, to be stripped from    │
│                                             the end of the template.                                                 │
│ --newline-sequence                    TEXT  The sequence that starts a newline. The default is tailored for          │
│                                             UNIX-like systems (Linux/macOS).                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Jinja Delimiters ───────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --delimiter-block-start       TEXT  The string marking the beginning of a block.                                     │
│                                     [default: {%]                                                                    │
│ --delimiter-block-end         TEXT  The string marking the end of a block.                                           │
│                                     [default: %}]                                                                    │
│ --delimiter-comment-start     TEXT  The string marking the beginning of a comment.                                   │
│                                     [default: {#]                                                                    │
│ --delimiter-comment-end       TEXT  The string marking the end of a comment.                                         │
│                                     [default: #}]                                                                    │
│ --delimiter-variable-start    TEXT  The string marking the beginning of a print statement.                           │
│                                     [default: {{]                                                                    │
│ --delimiter-variable-end      TEXT  The string marking the end of a print statement.                                 │
│                                     [default: }}]                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Jinja Prefixes ─────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --prefix-line-statement    TEXT  If given and a string, this will be used as prefix for line based statements.       │
│ --prefix-line-comment      TEXT  If given and a string, this will be used as prefix for line based comments.         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version      Show the version and exit.                                                                            │
│ --help         Show this message and exit.                                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```
