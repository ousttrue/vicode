'''
https://microsoft.github.io/language-server-protocol/specifications/specification-current/#uri
'''
from typing import TypedDict, List, Any, Dict, TypeAlias, Union
from enum import IntEnum


class Position(TypedDict):
    '''
    https://microsoft.github.io/language-server-protocol/specifications/specification-current/#position
    '''

    '''
    Line position in a document (zero-based).
    '''
    line: int

    '''
	Character offset on a line in a document (zero-based). Assuming that
	the line is represented as a string, the `character` value represents
	the gap between the `character` and `character + 1`.
		If the character value is greater than the line length it defaults back
	to the line length.
	'''
    character: int


class Range(TypedDict):
    '''
    https://microsoft.github.io/language-server-protocol/specifications/specification-current/#range
    '''

    '''
    The range's start position.
    '''
    start: Position

    '''
    The range's end position.
    '''
    end: Position


class Location(TypedDict):
    uri: str
    range: Range


class LocationLinkOptional(TypedDict, total=False):
    '''
    Span of the origin of this link.

    Used as the underlined span for mouse interaction. Defaults to the word
    range at the mouse position.
    '''
    originSelectionRange: Range


class LocationLinkRequired(TypedDict):
    '''
    The target resource identifier of this link.
    '''
    targetUri: str

    '''
     The full target range of this link. If the target for example is a symbol
     then target range is the range enclosing this symbol not including
     leading/trailing whitespace but everything else like comments. This
     information is typically used to highlight the range in the editor.
    '''
    targetRange: Range

    '''
     The range that should be selected and revealed when this link is being
     followed, e.g the name of a function. Must be contained by the the
     `targetRange`. See also `DocumentSymbol#range`
    '''
    targetSelectionRange: Range


class LocationLink(LocationLinkRequired, LocationLinkOptional):
    '''
    https://microsoft.github.io/language-server-protocol/specifications/specification-current/#locationLink
    '''


class DiagnosticSeverity(IntEnum):
    '''
    Reports an error.
    '''
    Error = 1
    '''
    Reports a warning.
    '''
    Warning = 2
    '''
    Reports an information.
    '''
    Information = 3
    '''
    Reports a hint.
    '''
    Hint = 4


class DiagnosticTag(IntEnum):
    '''
    The diagnostic tags.

    @since 3.15.0
    '''
    '''
    Unused or unnecessary code.

    Clients are allowed to render diagnostics with this tag faded out
    instead of having an error squiggle.
    '''
    Unnecessary = 1
    '''
    Deprecated or obsolete code.

    Clients are allowed to rendered diagnostics with this tag strike through.
    '''
    Deprecated = 2


class DiagnosticRelatedInformation(TypedDict):
    '''
    Represents a related message and source code location for a diagnostic.
    This should be used to point to code locations that cause or are related to
    a diagnostics, e.g when duplicating a symbol in a scope.
    '''

    '''
    The location of this related diagnostic information.
    '''
    location: Location

    '''
    The message of this related diagnostic information.
    '''
    message: str


class CodeDescription(TypedDict):
    '''
    Structure to capture a description for an error code.

    @since 3.16.0
    '''

    '''
    An URI to open with more information about the diagnostic error.
    '''
    href: str


class DiagnosticOptional(TypedDict, total=False):
    '''
    The diagnostic's severity. Can be omitted. If omitted it is up to the
    client to interpret diagnostics as error, warning, info or hint.
    '''
    severity: DiagnosticSeverity

    '''
    The diagnostic's code, which might appear in the user interface.
    '''
    code: int | str

    '''
    An optional property to describe the error code.

    @since 3.16.0
    '''
    codeDescription: CodeDescription

    '''
     A human-readable string describing the source of this
     diagnostic, e.g. 'typescript' or 'super lint'.
    '''
    source: str

    '''
     Additional metadata about the diagnostic.

     @since 3.15.0
    '''
    tags: List[DiagnosticTag]

    '''
     An array of related diagnostic information, e.g. when symbol-names within
     a scope collide all definitions can be marked via this property.
    '''
    relatedInformation: List[DiagnosticRelatedInformation]

    '''
     A data entry field that is preserved between a
     `textDocument/publishDiagnostics` notification and
     `textDocument/codeAction` request.

     @since 3.16.0
    '''
    data: Any


class DiagnosticRequired(TypedDict):
    '''
     The range at which the message applies.
    '''
    range: Range

    '''
     The diagnostic's message.
    '''
    message: str


class Diagnostic(DiagnosticRequired, DiagnosticOptional):
    '''
    https://microsoft.github.io/language-server-protocol/specifications/specification-current/#diagnostic
    '''


class CommandOptional(TypedDict):
    '''
    Arguments that the command handler should be
    invoked with.
    '''
    arguments: List[Any]


class CommandRequired(TypedDict):
    '''
    Title of the command, like `save`.
    '''
    title: str
    '''
    The identifier of the actual command handler.
    '''
    command: str


class Command(CommandRequired, CommandOptional):
    '''
    https://microsoft.github.io/language-server-protocol/specifications/specification-current/#command
    '''


class TextEdit(TypedDict):
    '''
    The range of the text document to be manipulated. To insert
    text into a document create a range where start === end.
    '''
    range: Range

    '''
    The string to be inserted. For delete operations use an
    empty string.
    '''
    newText: str


class ChangeAnnotationOptional(TypedDict):
    '''
    A flag which indicates that user confirmation is needed
    before applying the change.
    '''
    needsConfirmation: bool

    '''
    A human-readable string which is rendered less prominent in
    the user interface.
    '''
    description: str


class ChangeAnnotationRequired(TypedDict):
    '''
    Additional information that describes document changes.

    @since 3.16.0
    '''

    '''
    A human-readable string describing the actual change. The string
    is rendered prominent in the user interface.
    '''
    label: str


class ChangeAnnotation(ChangeAnnotationRequired, ChangeAnnotationOptional):
    '''

    '''


class AnnotatedTextEdit(TextEdit):
    '''
    A special text edit with an additional change annotation.

    @since 3.16.0
    '''

    '''
    The actual annotation identifier.
    '''
    annotationId: str


class CreateFileOptions(TypedDict, total=False):
    '''
    Options to create a file.
    '''

    '''
    Overwrite existing file. Overwrite wins over `ignoreIfExists`
    '''
    overwrite: bool

    '''
    Ignore if exists.
    '''
    ignoreIfExists: bool


class CreateFileOptional(TypedDict, total=False):
    '''
    Additional options
    '''
    options: CreateFileOptions

    '''
    An optional annotation identifer describing the operation.

    @since 3.16.0
    '''
    annotationId: str


class CreateFileRequired(TypedDict):
    '''
    Create file operation
    '''

    '''
    A create
    '''
    kind: str

    '''
    The resource to create.
    '''
    uri: str


class CreateFile(CreateFileRequired, CreateFileOptional):
    pass


class RenameFileOptions(TypedDict, total=False):
    '''
    Rename file options
    '''
    '''
    Overwrite target if existing. Overwrite wins over `ignoreIfExists`
    '''
    overwrite: bool

    '''
    Ignores if target exists.
    '''
    ignoreIfExists: bool


class RenameFileOptional(TypedDict):
    '''
    Rename options.
    '''
    options: RenameFileOptions

    '''
    An optional annotation identifer describing the operation.

    @since 3.16.0
    '''
    annotationId: str


class RenameFileRequired(TypedDict):
    '''
    Rename file operation
    '''
    '''
    A rename
    '''
    kind: str

    '''
    The old (existing) location.
    '''
    oldUri: str

    '''
    The new location.
    '''
    newUri: str


class RenameFile(RenameFileRequired, RenameFileOptional):
    pass


class DeleteFileOptions(TypedDict, total=False):
    '''
    Delete file options
    '''

    '''
    Delete the content recursively if a folder is denoted.
    '''
    recursive: bool

    '''
    Ignore the operation if the file doesn't exist.
    '''
    ignoreIfNotExists: bool


class DeleteFileOptional(TypedDict):
    '''
    Delete options.
    '''
    options: DeleteFileOptions

    '''
    An optional annotation identifer describing the operation.

    @since 3.16.0
    '''
    annotationId: str


class DeleteFileRequired(TypedDict):
    '''
    Delete file operation
    '''

    '''
    A delete
    '''
    kind: str

    '''
    The file to delete.
    '''
    uri: str


class DeleteFile(DeleteFileRequired, DeleteFileOptional):
    pass


class GroupOnLabel(TypedDict):
    '''
    Whether the client groups edits with equal labels into tree nodes,
    for instance all edits labelled with "Changes in Strings" would
    be a tree node.
    '''
    groupsOnLabel: bool


class WorkspaceEditClientCapabilities(TypedDict, total=False):
    '''
    The client supports versioned document changes in `WorkspaceEdit`s
    '''
    documentChanges: bool

    '''
    The resource operations the client supports. Clients should at least
    support 'create', 'rename' and 'delete' files and folders.

    @since 3.13.0
    '''
    resourceOperations: List[str]
    # /**
    #  * The kind of resource operations supported by the client.
    #  */
    # export type ResourceOperationKind = 'create' | 'rename' | 'delete';

    '''
    The failure handling strategy of a client if applying the workspace edit
    fails.

    @since 3.13.0
    '''
    failureHandling: str

    '''
    Whether the client normalizes line endings to the client specific
    setting.
    If set to `true` the client will normalize line ending characters
    in a workspace edit to the client specific new line character(s).

    @since 3.16.0
    '''
    normalizesLineEndings: bool

    '''
    Whether the client in general supports change annotations on text edits,
    create file, rename file and delete file changes.

    @since 3.16.0
    '''
    changeAnnotationSupport: GroupOnLabel


# export type FailureHandlingKind = 'abort' | 'transactional' | 'undo'
# 	| 'textOnlyTransactional';

# export namespace FailureHandlingKind {

# 	/**
# 	 * Applying the workspace change is simply aborted if one of the changes
# 	 * provided fails. All operations executed before the failing operation
# 	 * stay executed.
# 	 */
# 	export const Abort: FailureHandlingKind = 'abort';

# 	/**
# 	 * All operations are executed transactional. That means they either all
# 	 * succeed or no changes at all are applied to the workspace.
# 	 */
# 	export const Transactional: FailureHandlingKind = 'transactional';


# 	/**
# 	 * If the workspace edit contains only textual file changes they are
# 	 * executed transactional. If resource changes (create, rename or delete
# 	 * file) are part of the change the failure handling strategy is abort.
# 	 */
# 	export const TextOnlyTransactional: FailureHandlingKind
# 		= 'textOnlyTransactional';

# 	/**
# 	 * The client tries to undo the operations already executed. But there is no
# 	 * guarantee that this is succeeding.
# 	 */
# 	export const Undo: FailureHandlingKind = 'undo';
# }


class TextDocumentIdentifier(TypedDict):
    '''
    The text document's URI.
    '''
    uri: str


class TextDocumentItem(TypedDict):
    '''
    The text document's URI.
    '''
    uri: str

    '''
    The text document's language identifier.
    '''
    languageId: str

    '''
    The version number of this document (it will increase after each
    change, including undo/redo).
    '''
    version: int

    '''
    The content of the opened text document.
    '''
    text: str


class VersionedTextDocumentIdentifier(TextDocumentIdentifier):
    '''
    The version number of this document.

    The version number of a document will increase after each change,
    including undo/redo. The number doesn't need to be consecutive.
    '''
    version: int


class OptionalVersionedTextDocumentIdentifier(TextDocumentIdentifier, total=False):
    '''
    The version number of this document. If an optional versioned text document
    identifier is sent from the server to the client and the file is not
    open in the editor (the server has not received an open notification
    before) the server can send `null` to indicate that the version is
    known and the content on disk is the master (as specified with document
    content ownership).

    The version number of a document will increase after each change,
    including undo/redo. The number doesn't need to be consecutive.
    '''
    version: int


class TextDocumentEdit(TypedDict):
    '''
    The text document to change.
    '''
    textDocument: OptionalVersionedTextDocumentIdentifier

    '''
    The edits to be applied.

    @since 3.16.0 - support for AnnotatedTextEdit. This is guarded by the
    client capability `workspace.workspaceEdit.changeAnnotationSupport`
    '''
    edits: List[TextEdit | AnnotatedTextEdit]


class WorkspaceEdit(TypedDict, total=False):
    '''
    https://microsoft.github.io/language-server-protocol/specifications/specification-current/#workspaceEdit
    '''

    '''
    Holds changes to existing resources.
    '''
    changes: Dict[str, List[TextEdit]]

    '''
    Depending on the client capability
    `workspace.workspaceEdit.resourceOperations` document changes are either
    an array of `TextDocumentEdit`s to express changes to n different text
    documents where each text document edit addresses a specific version of
    a text document. Or it can contain above `TextDocumentEdit`s mixed with
    create, rename and delete file / folder operations.

    Whether a client supports versioned document edits is expressed via
    `workspace.workspaceEdit.documentChanges` client capability.

    If a client neither supports `documentChanges` nor
    `workspace.workspaceEdit.resourceOperations` then only plain `TextEdit`s
    using the `changes` property are supported.
    '''
    documentChanges: (
        List[TextDocumentEdit] |
        List[TextDocumentEdit | CreateFile | RenameFile | DeleteFile]
    )

    '''
    A map of change annotations that can be referenced in
    `AnnotatedTextEdit`s or create, rename and delete file / folder
    operations.

    Whether clients honor this property depends on the client capability
    `workspace.changeAnnotationSupport`.

    @since 3.16.0
    '''
    changeAnnotations: Dict[str, ChangeAnnotation]


class TextDocumentPositionParams(TypedDict):
    '''
    The text document.
    '''
    textDocument: TextDocumentIdentifier

    '''
    The position inside the text document.
    '''
    position: Position


class DocumentFilter(TypedDict, total=False):
    '''
    A language id, like `typescript`.
    '''
    language: str

    '''
    A Uri [scheme](#Uri.scheme), like `file` or `untitled`.
    '''
    scheme: str

    '''
    A glob pattern, like `*.{ts,js}`.

    Glob patterns can have the following syntax:
    - `*` to match one or more characters in a path segment
    - `?` to match on one character in a path segment
    - `**` to match any number of path segments, including none
    - `{}` to group sub patterns into an OR expression. (e.g. `**​/*.{ts,js}`
      matches all TypeScript and JavaScript files)
    - `[]` to declare a range of characters to match in a path segment
      (e.g., `example.[0-9]` to match on `example.0`, `example.1`, …)
    - `[!...]` to negate a range of characters to match in a path segment
      (e.g., `example.[!0-9]` to match on `example.a`, `example.b`, but
      not `example.0`)
    '''
    pattern: str


DocumentSelector: TypeAlias = List[DocumentFilter]


class StaticRegistrationOptions(TypedDict, total=False):
    '''
    Static registration options to be returned in the initialize request.
    '''
    '''
    The id used to register the request. The id can be used to deregister
    the request again. See also Registration#id.
    '''
    id: str


class TextDocumentRegistrationOptions(TypedDict, total=False):
    '''
    General text document registration options.
    '''
    '''
    A document selector to identify the scope of the registration. If set to
    null the document selector provided on the client side will be used.
    '''
    documentSelector: DocumentSelector


class MarkupContent(TypedDict):
    '''
    A `MarkupContent` literal represents a string value which content is
    interpreted base on its kind flag. Currently the protocol supports
    `plaintext` and `markdown` as markup kinds.

    If the kind is `markdown` then the value can contain fenced code blocks like
    in GitHub issues.

    Here is an example how such a string can be constructed using
    JavaScript / TypeScript:
    ```typescript
    let markdown: MarkdownContent = {
        kind: MarkupKind.Markdown,
        value: [
                '# Header',
                'Some text',
                '```typescript',
                'someCode();',
                '```'
        ].join('\n')
    };
    ```

   Please Note* that clients might sanitize the return markdown. A client could
    decide to remove HTML from the markdown to avoid script execution.
    '''
    '''
    The type of the Markup
    '''
    kind: str
    # export type MarkupKind = 'plaintext' | 'markdown';

    '''
    The content itself
    '''
    value: str


class MarkdownClientCapabilitiesOptional(TypedDict):
    '''
    The version of the parser.
    '''
    version: str


class MarkdownClientCapabilitiesRequired(TypedDict):
    '''
    The name of the parser.
    '''
    parser: str


class MarkdownClientCapabilities(MarkdownClientCapabilitiesRequired, MarkdownClientCapabilitiesOptional):
    '''
    Client capabilities specific to the used markdown parser.

    @since 3.16.0
    '''


class WorkDoneProgressBeginOptional(TypedDict, total=False):
    '''
    Controls if a cancel button should show to allow the user to cancel the
    long running operation. Clients that don't support cancellation are
    allowed to ignore the setting.
    '''
    cancellable: bool

    '''
    Optional, more detailed associated progress message. Contains
    complementary information to the `title`.

    Examples: "3/25 files", "project/src/module2", "node_modules/some_dep".
    If unset, the previous progress message (if any) is still valid.
    '''
    message: str

    '''
    Optional progress percentage to display (value 100 is considered 100%).
    If not provided infinite progress is assumed and clients are allowed
    to ignore the `percentage` value in subsequent in report notifications.

    The value should be steadily rising. Clients are free to ignore values
    that are not following this rule. The value range is [0, 100]
    '''
    percentage: int


class WorkDoneProgressBeginRequired(TypedDict):
    kind: str

    '''
    Mandatory title of the progress operation. Used to briefly inform about
    the kind of operation being performed.

    Examples: "Indexing" or "Linking dependencies".
    '''
    title: str


class WorkDoneProgressBegin(WorkDoneProgressBeginRequired, WorkDoneProgressBeginOptional):
    pass


class WorkDoneProgressReport(TypedDict, total=False):

    kind: str

    '''
    Controls enablement state of a cancel button. This property is only valid
    if a cancel button got requested in the `WorkDoneProgressBegin` payload.
   
    Clients that don't support cancellation or don't support control the
    button's enablement state are allowed to ignore the setting.
    '''
    cancellable: bool

    '''
    Optional, more detailed associated progress message. Contains
    complementary information to the `title`.
   
    Examples: "3/25 files", "project/src/module2", "node_modules/some_dep".
    If unset, the previous progress message (if any) is still valid.
    '''
    message: str

    '''
    Optional progress percentage to display (value 100 is considered 100%).
    If not provided infinite progress is assumed and clients are allowed
    to ignore the `percentage` value in subsequent in report notifications.
   
    The value should be steadily rising. Clients are free to ignore values
    that are not following this rule. The value range is [0, 100]
    '''
    percentage: int


class WorkDoneProgressEnd(TypedDict, total=False):

    kind: str

    '''
    Optional, a final message indicating to for example indicate the outcome
    of the operation.
    '''
    message: str


ProgressToken: TypeAlias = Union[int, str]


class WorkDoneProgressParams(TypedDict, total=False):
    '''
    An optional token that a server can use to report work done progress.
    '''
    workDoneToken: ProgressToken
