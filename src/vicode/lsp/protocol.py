from typing import Optional, TypedDict, Any, List
from .basic_structures import *


class ClientInfo(TypedDict):
    '''
    The name of the client as defined by the client.
    '''
    name: str

    '''
    The client's version as defined by the client.
    '''
    version: Optional[str]


class WorkspaceFolder(TypedDict):
    '''
    The associated URI for this workspace folder.
    '''
    uri: str

    '''
    The name of the workspace folder. Used to refer to this
    workspace folder in the user interface.
    '''
    name: str


class InitializeParamsOptinal(TypedDict, total=False):
    '''
    Information about the client

    @since 3.15.0
    '''
    clientInfo: ClientInfo

    '''
    The locale the client is currently showing the user interface
    in. This must not necessarily be the locale of the operating
    system.

    Uses IETF language tags as the value's syntax
    (See https://en.wikipedia.org/wiki/IETF_language_tag)

    @since 3.16.0
    '''
    locale: str

    '''
    The rootPath of the workspace. Is null
    if no folder is open.

    @deprecated in favour of `rootUri`.
    '''
    rootPath: str

    '''
    The rootUri of the workspace. Is null if no
    folder is open. If both `rootPath` and `rootUri` are set
    `rootUri` wins.

    @deprecated in favour of `workspaceFolders`
    '''
    rootUri: str

    '''
    User provided initialization options.
    '''
    initializationOptions: Any

    '''
    The initial trace setting. If omitted trace is disabled ('off').
    '''
    trace: str
    # export type TraceValue = 'off' | 'messages' | 'verbose'

    '''
    The workspace folders configured in the client when the server starts.
    This property is only available if the client supports workspace folders.
    It can be `null` if the client supports workspace folders but none are
    configured.

    @since 3.6.0
    '''
    workspaceFolders: List[WorkspaceFolder]


class FileOperation(TypedDict, total=False):
    '''
    Whether the client supports dynamic registration for file
    requests/notifications.
    '''
    dynamicRegistration: bool

    '''
    The client has support for sending didCreateFiles notifications.
    '''
    didCreate: bool

    '''
    The client has support for sending willCreateFiles requests.
    '''
    willCreate: bool

    '''
    The client has support for sending didRenameFiles notifications.
    '''
    didRename: bool

    '''
    The client has support for sending willRenameFiles requests.
    '''
    willRename: bool

    '''
    The client has support for sending didDeleteFiles notifications.
    '''
    didDelete: bool

    '''
    The client has support for sending willDeleteFiles requests.
    '''
    willDelete: bool


class DidChangeConfigurationClientCapabilities(TypedDict, total=False):
    '''
    Did change configuration notification supports dynamic registration.
    '''
    dynamicRegistration: bool


class DidChangeWatchedFilesClientCapabilities(TypedDict, total=False):
    '''
    Did change watched files notification supports dynamic registration.
    Please note that the current protocol doesn't support static
    configuration for file changes from the server side.
    '''
    dynamicRegistration: bool


class SymbolKind(TypedDict, total=False):
    '''
    The symbol kind values the client supports. When this
    property exists the client also guarantees that it will
    handle values outside its set gracefully and falls back
    to a default value when unknown.

    If this property is not present the client only supports
    the symbol kinds from `File` to `Array` as defined in
    the initial version of the protocol.
    '''
    valueSet: List[str]


class CompletionItemTag(IntEnum):
    '''
    Completion item tags are extra annotations that tweak the rendering of a
    completion item.

    @since 3.15.0
    '''

    '''
    Render a completion as obsolete, usually using a strike-out.
    '''
    Deprecated = 1


class TagSupport(TypedDict, total=False):
    '''
    The tags supported by the client.
    '''
    valueSet: List[CompletionItemTag]


class ResolveSupport(TypedDict):
    '''
    The properties that a client can resolve lazily.
    '''
    properties: List[str]


class WorkspaceSymbolClientCapabilities(TypedDict, total=False):
    '''
    Symbol request supports dynamic registration.
    '''
    dynamicRegistration: bool

    '''
    Specific capabilities for the `SymbolKind` in the `workspace/symbol`
    request.
    '''
    symbolKind: SymbolKind

    '''
    The client supports tags on `SymbolInformation` and `WorkspaceSymbol`.
    Clients supporting tags have to handle unknown tags gracefully.
   
    @since 3.16.0
    '''
    tagSupport: TagSupport

    '''
    The client support partial workspace symbols. The client will send the
    request `workspaceSymbol/resolve` to the server to resolve additional
    properties.
   
    @since 3.17.0 - proposedState
    '''
    resolveSupport: ResolveSupport


class ExecuteCommandClientCapabilities(TypedDict, total=False):
    '''
    Execute command supports dynamic registration.
    '''
    dynamicRegistration: bool


class SemanticTokensWorkspaceClientCapabilities(TypedDict, total=False):
    '''
    Whether the client implementation supports a refresh request sent from
    the server to the client.

    Note that this event is global and will force the client to refresh all
    semantic tokens currently shown. It should be used with absolute care
    and is useful for situation where a server for example detect a project
    wide change that requires such a calculation.
    '''
    refreshSupport: bool


class CodeLensWorkspaceClientCapabilities(TypedDict, total=False):
    '''
    Whether the client implementation supports a refresh request sent from the
    server to the client.

    Note that this event is global and will force the client to refresh all
    code lenses currently shown. It should be used with absolute care and is
    useful for situation where a server for example detect a project wide
    change that requires such a calculation.
    '''
    refreshSupport: bool


class WorkSpace(TypedDict, total=False):
    '''
    The client supports applying batch edits
    to the workspace by supporting the request
    'workspace/applyEdit'
    '''
    applyEdit: bool

    '''
    Capabilities specific to `WorkspaceEdit`s
    '''
    workspaceEdit: WorkspaceEditClientCapabilities

    '''
    Capabilities specific to the `workspace/didChangeConfiguration`
    notification.
    '''
    didChangeConfiguration: DidChangeConfigurationClientCapabilities

    '''
    Capabilities specific to the `workspace/didChangeWatchedFiles`
    notification.
    '''
    didChangeWatchedFiles: DidChangeWatchedFilesClientCapabilities

    '''
    Capabilities specific to the `workspace/symbol` request.
    '''
    symbol: WorkspaceSymbolClientCapabilities

    '''
    Capabilities specific to the `workspace/executeCommand` request.
    '''
    executeCommand: ExecuteCommandClientCapabilities

    '''
    The client has support for workspace folders.

    @since 3.6.0
    '''
    workspaceFolders: bool

    '''
    The client supports `workspace/configuration` requests.

    @since 3.6.0
    '''
    configuration: bool

    '''
    Capabilities specific to the semantic token requests scoped to the
    workspace.

    @since 3.16.0
    '''
    semanticTokens: SemanticTokensWorkspaceClientCapabilities

    '''
    Capabilities specific to the code lens requests scoped to the
    workspace.

    @since 3.16.0
    '''
    codeLens: CodeLensWorkspaceClientCapabilities

    '''
    The client has support for file requests/notifications.

    @since 3.16.0
    '''
    fileOperations: FileOperation


class MessageActionItem(TypedDict, total=False):
    '''
    Whether the client supports additional attributes which
    are preserved and sent back to the server in the
    request's response.
    '''
    additionalPropertiesSupport: bool


class ShowMessageRequestClientCapabilities(TypedDict, total=False):
    '''
    Show message request client capabilities
    '''

    '''
    Capabilities specific to the `MessageActionItem` type.
    '''
    messageActionItem: MessageActionItem


class ShowDocumentClientCapabilities(TypedDict):
    '''
    Client capabilities for the show document request.

    @since 3.16.0
    '''

    '''
    The client has support for the show document
    request.
    '''
    support: bool


class Window(TypedDict, total=False):
    '''
    It indicates whether the client supports server initiated
    progress using the `window/workDoneProgress/create` request.

    The capability also controls Whether client supports handling
    of progress notifications. If set servers are allowed to report a
    `workDoneProgress` property in the request specific server
    capabilities.

    @ since 3.15.0
    '''
    workDoneProgress: bool

    '''
    Capabilities specific to the showMessage request

    @ since 3.16.0
    '''
    showMessage: ShowMessageRequestClientCapabilities

    '''
    Client capabilities for the show document request.

    @ since 3.16.0
    '''
    showDocument: ShowDocumentClientCapabilities


class StaleRequestSupport(TypedDict):
    '''
    The client will actively cancel the request.
    '''
    cancel: bool

    '''
    The list of requests for which the client
    will retry the request if it receives a
    response with error code `ContentModified``
    '''
    retryOnContentModified: List[str]


class RegularExpressionsClientCapabilities(TypedDict):
    '''
    Client capabilities specific to regular expressions.
    '''
    '''
    The engine's name.
    '''
    engine: str

    '''
    The engine's version.
    '''
    version: Optional[str]


class General(TypedDict, total=False):
    '''
    Client capability that signals how the client
    handles stale requests(e.g. a request
    for which the client will not process the response
    anymore since the information is outdated).

    @ since 3.17.0
    '''
    staleRequestSupport: StaleRequestSupport

    '''
    Client capabilities specific to regular expressions.

    @ since 3.16.0
    '''
    regularExpressions: RegularExpressionsClientCapabilities

    '''
    Client capabilities specific to the client's markdown parser.

    @ since 3.16.0
    '''
    markdown: MarkdownClientCapabilities


class TextDocumentSyncClientCapabilities(TypedDict, total=False):
    '''
    Whether text document synchronization supports dynamic registration.
    '''
    dynamicRegistration: bool

    '''
    The client supports sending will save notifications.
    '''
    willSave: bool

    '''
    The client supports sending a will save request and
    waits for a response providing text edits which will
    be applied to the document before it is saved.
    '''
    willSaveWaitUntil: bool

    '''
    The client supports did save notifications.
    '''
    didSave: bool


class InsertTextMode(IntEnum):
    '''
    How whitespace and indentation is handled during completion
    item insertion.

    @since 3.16.0
    '''

    '''
    The insertion or replace strings is taken as it is. If the
    value is multi line the lines below the cursor will be
    inserted using the indentation defined in the string value.
    The client will not apply any kind of adjustments to the
    string.
    '''
    asIs = 1

    '''
    The editor adjusts leading whitespace of new lines so that
    they match the indentation up to the cursor of the line for
    which the item is accepted.
   
    Consider a line like this: <2tabs><cursor><3tabs>foo. Accepting a
    multi line completion item is indented using 2 tabs and all
    following lines inserted will be indented using 2 tabs as well.
    '''
    adjustIndentation = 2


class InsertTextModeSupport(TypedDict):
    valueSet: List[InsertTextMode]


class CompletionItem(TypedDict, total=False):
    '''
    Client supports snippets as insert text.

    A snippet can define tab stops and placeholders with `$1`, `$2`
    and `${3:foo}`. `$0` defines the final tab stop, it defaults to
    the end of the snippet. Placeholders with equal identifiers are
    linked, that is typing in one will update others too.
    '''
    snippetSupport: bool

    '''
    Client supports commit characters on a completion item.
    '''
    commitCharactersSupport: bool

    '''
    Client supports the follow content formats for the documentation
    property. The order describes the preferred format of the client.
    '''
    documentationFormat: List[str]

    '''
    Client supports the deprecated property on a completion item.
    '''
    deprecatedSupport: bool

    '''
    Client supports the preselect property on a completion item.
    '''
    preselectSupport: bool

    '''
    Client supports the tag property on a completion item. Clients
    supporting tags have to handle unknown tags gracefully. Clients
    especially need to preserve unknown tags when sending a completion
    item back to the server in a resolve call.

    @since 3.15.0
    '''
    tagSupport: TagSupport

    '''
    Client supports insert replace edit to control different behavior if
    a completion item is inserted in the text or should replace text.

    @since 3.16.0
    '''
    insertReplaceSupport: bool

    '''
    Indicates which properties a client can resolve lazily on a
    completion item. Before version 3.16.0 only the predefined properties
    `documentation` and `detail` could be resolved lazily.

    @since 3.16.0
    '''
    resolveSupport: ResolveSupport

    '''
    The client supports the `insertTextMode` property on
    a completion item to override the whitespace handling mode
    as defined by the client (see `insertTextMode`).

    @since 3.16.0
    '''
    insertTextModeSupport: InsertTextModeSupport

    '''
    The client has support for completion item label
    details (see also `CompletionItemLabelDetails`).

    @since 3.17.0 - proposed state
    '''
    labelDetailsSupport: bool


class CompletionItemKind(TypedDict, total=False):
    '''
    The completion item kind values the client supports. When this
    property exists the client also guarantees that it will
    handle values outside its set gracefully and falls back
    to a default value when unknown.

    If this property is not present the client only supports
    the completion items kinds from `Text` to `Reference` as defined in
    the initial version of the protocol.
    '''
    valueSet: List[str]


class CompletionList(TypedDict, total=False):
    '''
    The client supports the the following itemDefaults on
    a completion list.

    The value lists the supported property names of the
    `CompletionList.itemDefaults` object. If omitted
    no properties are supported.

    @since 3.17.0 - proposed state
    '''
    itemDefaults: List[str]


class CompletionClientCapabilities(TypedDict, total=False):
    '''
    Whether completion supports dynamic registration.
    '''
    dynamicRegistration: bool

    '''
    The client supports the following `CompletionItem` specific
    capabilities.
    '''
    completionItem: CompletionItem

    completionItemKind: CompletionItemKind

    '''
    The client supports to send additional context information for a
    `textDocument/completion` request.
    '''
    contextSupport: bool

    '''
    The client's default when the completion item doesn't provide a
    `insertTextMode` property.

    @since 3.17.0 - proposed state
    '''
    insertTextMode: InsertTextMode

    '''
    The client supports the following `CompletionList` specific
    capabilities.

    @since 3.17.0 - proposed state
    '''
    completionList: CompletionList


class HoverClientCapabilities(TypedDict, total=False):
    '''
    Whether hover supports dynamic registration.
    '''
    dynamicRegistration: bool

    '''
    Client supports the follow content formats if the content
    property refers to a `literal of type MarkupContent`.
    The order describes the preferred format of the client.
    '''
    contentFormat: List[str]


class ParameterInformation(TypedDict, total=False):
    '''
    The client supports processing label offsets instead of a
    simple label string.

    @since 3.14.0
    '''
    labelOffsetSupport: bool


class SignatureInformation(TypedDict, total=False):
    '''
    Client supports the follow content formats for the documentation
    property. The order describes the preferred format of the client.
    '''
    documentationFormat: List[str]

    '''
    Client capabilities specific to parameter information.
    '''
    parameterInformation: ParameterInformation

    '''
    The client supports the `activeParameter` property on
    `SignatureInformation` literal.

    @since 3.16.0
    '''
    activeParameterSupport: bool


class SignatureHelpClientCapabilities(TypedDict, total=False):
    '''
    Whether signature help supports dynamic registration.
    '''
    dynamicRegistration: bool

    '''
    The client supports the following `SignatureInformation`
    specific properties.
    '''
    signatureInformation: SignatureInformation

    '''
    The client supports to send additional context information for a
    `textDocument/signatureHelp` request. A client that opts into
    contextSupport will also support the `retriggerCharacters` on
    `SignatureHelpOptions`.

    @since 3.15.0
    '''
    contextSupport: bool


class DeclarationClientCapabilities(TypedDict, total=False):
    '''
    Whether declaration supports dynamic registration. If this is set to
    `true` the client supports the new `DeclarationRegistrationOptions`
    return value for the corresponding server capability as well.
    '''
    dynamicRegistration: bool

    '''
    The client supports additional metadata in the form of declaration links.
    '''
    linkSupport: bool


class DefinitionClientCapabilities(TypedDict, total=False):
    '''
    Whether definition supports dynamic registration.
    '''
    dynamicRegistration: bool

    '''
    The client supports additional metadata in the form of definition links.

    @since 3.14.0
    '''
    linkSupport: bool


class TypeDefinitionClientCapabilities(TypedDict, total=False):
    '''
    Whether implementation supports dynamic registration. If this is set to
    `true` the client supports the new `TypeDefinitionRegistrationOptions`
    return value for the corresponding server capability as well.
    '''
    dynamicRegistration: bool

    '''
    The client supports additional metadata in the form of definition links.

    @since 3.14.0
    '''
    linkSupport: bool


class ImplementationClientCapabilities(TypedDict, total=False):
    '''
    Whether implementation supports dynamic registration. If this is set to
    `true` the client supports the new `ImplementationRegistrationOptions`
    return value for the corresponding server capability as well.
    '''
    dynamicRegistration: bool

    '''
    The client supports additional metadata in the form of definition links.

    @since 3.14.0
    '''
    linkSupport: bool


class ReferenceClientCapabilities(TypedDict, total=False):
    '''
    Whether references supports dynamic registration.
    '''
    dynamicRegistration: bool


class DocumentHighlightClientCapabilities(TypedDict, total=False):
    '''
    Whether document highlight supports dynamic registration.
    '''
    dynamicRegistration: bool


class DocumentSymbolClientCapabilities(TypedDict, total=False):
    '''
    Whether document symbol supports dynamic registration.
    '''
    dynamicRegistration: bool

    '''
    Specific capabilities for the `SymbolKind` in the
    `textDocument/documentSymbol` request.
    '''
    symbolKind: SymbolKind

    '''
    The client supports hierarchical document symbols.
    '''
    hierarchicalDocumentSymbolSupport: bool

    '''
    The client supports tags on `SymbolInformation`. Tags are supported on
    `DocumentSymbol` if `hierarchicalDocumentSymbolSupport` is set to true.
    Clients supporting tags have to handle unknown tags gracefully.

    @since 3.16.0
    '''
    tagSupport: TagSupport

    '''
    The client supports an additional label presented in the UI when
    registering a document symbol provider.

    @since 3.16.0
    '''
    labelSupport: bool


class CodeActionKind(TypedDict):
    '''
    The code action kind values the client supports. When this
    property exists the client also guarantees that it will
    handle values outside its set gracefully and falls back
    to a default value when unknown.
    '''
    valueSet: List[str]


class CodeActionLiteralSupport(TypedDict):
    '''
    The code action kind is supported with the following value
    set.
    '''
    codeActionKind: CodeActionKind


class CodeActionClientCapabilities(TypedDict, total=False):
    '''
    Whether code action supports dynamic registration.
    '''
    dynamicRegistration: bool

    '''
    The client supports code action literals as a valid
    response of the `textDocument/codeAction` request.
   
    @since 3.8.0
    '''
    codeActionLiteralSupport: CodeActionLiteralSupport

    '''
    Whether code action supports the `isPreferred` property.
   
    @since 3.15.0
    '''
    isPreferredSupport: bool

    '''
    Whether code action supports the `disabled` property.
   
    @since 3.16.0
    '''
    disabledSupport: bool

    '''
    Whether code action supports the `data` property which is
    preserved between a `textDocument/codeAction` and a
    `codeAction/resolve` request.
   
    @since 3.16.0
    '''
    dataSupport: bool

    '''
    Whether the client supports resolving additional code action
    properties via a separate `codeAction/resolve` request.
   
    @since 3.16.0
    '''
    resolveSupport: ResolveSupport

    '''
    Whether the client honors the change annotations in
    text edits and resource operations returned via the
    `CodeAction#edit` property by for example presenting
    the workspace edit in the user interface and asking
    for confirmation.
   
    @since 3.16.0
    '''
    honorsChangeAnnotations: bool


class CodeLensClientCapabilities(TypedDict, total=False):
    '''
    Whether code lens supports dynamic registration.
    '''
    dynamicRegistration: bool


class DocumentLinkClientCapabilities(TypedDict, total=False):
    '''
    Whether document link supports dynamic registration.
    '''
    dynamicRegistration: bool

    '''
    Whether the client supports the `tooltip` property on `DocumentLink`.
   
    @since 3.15.0
    '''
    tooltipSupport: bool


class DocumentColorClientCapabilities(TypedDict, total=False):
    '''
    Whether document color supports dynamic registration.
    '''
    dynamicRegistration: bool


class DocumentFormattingClientCapabilities(TypedDict, total=False):
    '''
    Whether formatting supports dynamic registration.
    '''
    dynamicRegistration: bool


class DocumentRangeFormattingClientCapabilities(TypedDict, total=False):
    '''
    Whether formatting supports dynamic registration.
    '''
    dynamicRegistration: bool


class DocumentOnTypeFormattingClientCapabilities(TypedDict, total=False):
    '''
    Whether on type formatting supports dynamic registration.
    '''
    dynamicRegistration: bool


class PrepareSupportDefaultBehavior(IntEnum):
    '''
    The client's default behavior is to select the identifier
    according the to language's syntax rule.
    '''
    Identifier = 1


class RenameClientCapabilities(TypedDict, total=False):
    '''
    Whether rename supports dynamic registration.
    '''
    dynamicRegistration: bool

    '''
    Client supports testing for validity of rename operations
    before execution.
   
    @since version 3.12.0
    '''
    prepareSupport: bool

    '''
    Client supports the default behavior result
    (`{ defaultBehavior: bool }`).
   
    The value indicates the default behavior used by the
    client.
   
    @since version 3.16.0
    '''
    prepareSupportDefaultBehavior: PrepareSupportDefaultBehavior

    '''
    Whether th client honors the change annotations in
    text edits and resource operations returned via the
    rename request's workspace edit by for example presenting
    the workspace edit in the user interface and asking
    for confirmation.
   
    @since 3.16.0
    '''
    honorsChangeAnnotations: bool


class PublishDiagnosticsClientCapabilities(TypedDict, total=False):
    '''
    Whether the clients accepts diagnostics with related information.
    '''
    relatedInformation: bool

    '''
    Client supports the tag property to provide meta data about a diagnostic.
    Clients supporting tags have to handle unknown tags gracefully.
   
    @since 3.15.0
    '''
    tagSupport: TagSupport

    '''
    Whether the client interprets the version property of the
    `textDocument/publishDiagnostics` notification's parameter.
   
    @since 3.15.0
    '''
    versionSupport: bool

    '''
    Client supports a codeDescription property
   
    @since 3.16.0
    '''
    codeDescriptionSupport: bool

    '''
    Whether code action supports the `data` property which is
    preserved between a `textDocument/publishDiagnostics` and
    `textDocument/codeAction` request.
   
    @since 3.16.0
    '''
    dataSupport: bool


class FoldingRangeClientCapabilities(TypedDict, total=False):
    '''
    Whether implementation supports dynamic registration for folding range
    providers. If this is set to `true` the client supports the new
    `FoldingRangeRegistrationOptions` return value for the corresponding
    server capability as well.
    '''
    dynamicRegistration: bool

    '''
    The maximum number of folding ranges that the client prefers to receive
    per document. The value serves as a hint, servers are free to follow the
    limit.
    '''
    rangeLimit: int

    '''
    If set, the client signals that it only supports folding complete lines.
    If set, client will ignore specified `startCharacter` and `endCharacter`
    properties in a FoldingRange.
    '''
    lineFoldingOnly: bool


class SelectionRangeClientCapabilities(TypedDict, total=False):
    '''
    Whether implementation supports dynamic registration for selection range
    providers. If this is set to `true` the client supports the new
    `SelectionRangeRegistrationOptions` return value for the corresponding
    server capability as well.
    '''
    dynamicRegistration: bool


class LinkedEditingRangeClientCapabilities(TypedDict, total=False):
    '''
    Whether implementation supports dynamic registration.
    If this is set to `true` the client supports the new
    `(TextDocumentRegistrationOptions & StaticRegistrationOptions)`
    return value for the corresponding server capability as well.
    '''
    dynamicRegistration: bool


class Full(TypedDict, total=False):
    '''
    The client will send the `textDocument/semanticTokens/full/delta`
    request if the server provides a corresponding handler.
    '''
    delta: bool


class Requests(TypedDict, total=False):
    '''
    The client will send the `textDocument/semanticTokens/range` request
    if the server provides a corresponding handler.
    '''
    range: bool | dict

    '''
    The client will send the `textDocument/semanticTokens/full` request
    if the server provides a corresponding handler.
    '''
    full: bool | Full


class SemanticTokensClientCapabilities(TypedDict, total=False):
    '''
    Whether implementation supports dynamic registration. If this is set to
    `true` the client supports the new `(TextDocumentRegistrationOptions &
    StaticRegistrationOptions)` return value for the corresponding server
    capability as well.
    '''
    dynamicRegistration: bool

    '''
    Which requests the client supports and might send to the server
    depending on the server's capability. Please note that clients might not
    show semantic tokens or degrade some of the user experience if a range
    or full request is advertised by the client but not provided by the
    server. If for example the client capability `requests.full` and
    `request.range` are both set to true but the server only provides a
    range provider the client might not render a minimap correctly or might
    even decide to not show any semantic tokens at all.
    '''
    requests: Requests

    '''
    The token types that the client supports.
    '''
    tokenTypes: List[str]

    '''
    The token modifiers that the client supports.
    '''
    tokenModifiers: List[str]

    '''
    The formats the clients supports.
    '''
    formats: List[str]

    '''
    Whether the client supports tokens that can overlap each other.
    '''
    overlappingTokenSupport: bool

    '''
    Whether the client supports tokens that can span multiple lines.
    '''
    multilineTokenSupport: bool

    '''
    Whether the client allows the server to actively cancel a
    semantic token request, e.g. supports returning
    ErrorCodes.ServerCancelled. If a server does the client
    needs to retrigger the request.
   
    @since 3.17.0
    '''
    serverCancelSupport: bool

    '''
    Whether the client uses semantic tokens to augment existing
    syntax tokens. If set to `true` client side created syntax
    tokens and semantic tokens are both used for colorization. If
    set to `false` the client only uses the returned semantic tokens
    for colorization.
   
    If the value is `undefined` then the client behavior is not
    specified.
   
    @since 3.17.0
    '''
    augmentsSyntaxTokens: bool


class CallHierarchyClientCapabilities(TypedDict, total=False):
    '''
    Whether implementation supports dynamic registration. If this is set to
    `true` the client supports the new `(TextDocumentRegistrationOptions &
    StaticRegistrationOptions)` return value for the corresponding server
    capability as well.
    '''
    dynamicRegistration: bool


class MonikerClientCapabilities(TypedDict, total=False):
    '''
    Whether implementation supports dynamic registration. If this is set to
    `true` the client supports the new `(TextDocumentRegistrationOptions &
    StaticRegistrationOptions)` return value for the corresponding server
    capability as well.
    '''
    dynamicRegistration: bool


class TypeHierarchyClientCapabilities(TypedDict, total=False):
    '''
    Whether implementation supports dynamic registration. If this is set to
    `true` the client supports the new `(TextDocumentRegistrationOptions &
    StaticRegistrationOptions)` return value for the corresponding server
    capability as well.
    '''
    dynamicRegistration: bool


class InlineValueClientCapabilities(TypedDict, total=False):
    '''
    Client capabilities specific to inline values.

    @since 3.17.0 - proposed state
    '''

    '''
    Whether implementation supports dynamic registration for inline
    value providers.
    '''
    dynamicRegistration: bool


class InlayHintClientCapabilities(TypedDict, total=False):
    '''
    Inlay hint client capabilities.

    @since 3.17.0 - proposed state
    '''

    '''
    Whether inlay hints support dynamic registration.
    '''
    dynamicRegistration: bool

    '''
    Indicates which properties a client can resolve lazily on a inlay
    hint.
    '''
    resolveSupport: ResolveSupport


class TextDocumentClientCapabilities(TypedDict, total=False):
    '''
    Text document specific client capabilities.
    '''

    synchronization: TextDocumentSyncClientCapabilities

    '''
    Capabilities specific to the `textDocument/completion` request.
    '''
    completion: CompletionClientCapabilities

    '''
    Capabilities specific to the `textDocument/hover` request.
    '''
    hover: HoverClientCapabilities

    '''
    Capabilities specific to the `textDocument/signatureHelp` request.
    '''
    signatureHelp: SignatureHelpClientCapabilities

    '''
    Capabilities specific to the `textDocument/declaration` request.

    @since 3.14.0
    '''
    declaration: DeclarationClientCapabilities

    '''
    Capabilities specific to the `textDocument/definition` request.
    '''
    definition: DefinitionClientCapabilities

    '''
    Capabilities specific to the `textDocument/typeDefinition` request.

    @since 3.6.0
    '''
    typeDefinition: TypeDefinitionClientCapabilities

    '''
    Capabilities specific to the `textDocument/implementation` request.

    @since 3.6.0
    '''
    implementation: ImplementationClientCapabilities

    '''
    Capabilities specific to the `textDocument/references` request.
    '''
    references: ReferenceClientCapabilities

    '''
    Capabilities specific to the `textDocument/documentHighlight` request.
    '''
    documentHighlight: DocumentHighlightClientCapabilities

    '''
    Capabilities specific to the `textDocument/documentSymbol` request.
    '''
    documentSymbol: DocumentSymbolClientCapabilities

    '''
    Capabilities specific to the `textDocument/codeAction` request.
    '''
    codeAction: CodeActionClientCapabilities

    '''
    Capabilities specific to the `textDocument/codeLens` request.
    '''
    codeLens: CodeLensClientCapabilities

    '''
    Capabilities specific to the `textDocument/documentLink` request.
    '''
    documentLink: DocumentLinkClientCapabilities

    '''
    Capabilities specific to the `textDocument/documentColor` and the
    `textDocument/colorPresentation` request.

    @since 3.6.0
    '''
    colorProvider: DocumentColorClientCapabilities

    '''
    Capabilities specific to the `textDocument/formatting` request.
    '''
    formatting: DocumentFormattingClientCapabilities

    '''
    Capabilities specific to the `textDocument/rangeFormatting` request.
    '''
    rangeFormatting: DocumentRangeFormattingClientCapabilities

    ''' request.
    Capabilities specific to the `textDocument/onTypeFormatting` request.
    '''
    onTypeFormatting: DocumentOnTypeFormattingClientCapabilities

    '''
    Capabilities specific to the `textDocument/rename` request.
    '''
    rename: RenameClientCapabilities

    '''
    Capabilities specific to the `textDocument/publishDiagnostics`
    notification.
    '''
    publishDiagnostics: PublishDiagnosticsClientCapabilities

    '''
    Capabilities specific to the `textDocument/foldingRange` request.

    @since 3.10.0
    '''
    foldingRange: FoldingRangeClientCapabilities

    '''
    Capabilities specific to the `textDocument/selectionRange` request.

    @since 3.15.0
    '''
    selectionRange: SelectionRangeClientCapabilities

    '''
    Capabilities specific to the `textDocument/linkedEditingRange` request.

    @since 3.16.0
    '''
    linkedEditingRange: LinkedEditingRangeClientCapabilities

    '''
    Capabilities specific to the various call hierarchy requests.

    @since 3.16.0
    '''
    callHierarchy: CallHierarchyClientCapabilities

    '''
    Capabilities specific to the various semantic token requests.

    @since 3.16.0
    '''
    semanticTokens: SemanticTokensClientCapabilities

    '''
    Capabilities specific to the `textDocument/moniker` request.

    @since 3.16.0
    '''
    moniker: MonikerClientCapabilities

    '''
    Capabilities specific to the various type hierarchy requests.

    @since 3.17.0 - proposed state
    '''
    typeHierarchy: TypeHierarchyClientCapabilities

    '''
    Capabilities specific to the `textDocument/inlineValue` request.

    @since 3.17.0 - proposed state
    '''
    inlineValue: InlineValueClientCapabilities

    '''
    Capabilities specific to the `textDocument/inlayHint` request.

    @since 3.17.0 - proposed state
    '''
    inlayHint: InlayHintClientCapabilities


class ClientCapabilities(TypedDict, total=False):
    '''
    Workspace specific client capabilities.
    '''
    workspace: WorkSpace

    '''
    Text document specific client capabilities.
    '''
    textDocument: TextDocumentClientCapabilities

    '''
    Window specific client capabilities.
    '''
    window: Window

    '''
    General client capabilities.

    @ since 3.16.0
    '''
    general: General

    '''
    Experimental client capabilities.
    '''
    experimental: Any


class InitializeParams(WorkDoneProgressParams, InitializeParamsOptinal):
    '''
    https: // microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification /  # initialize
    '''

    '''
    The process Id of the parent process that started the server. Is null if
    the process has not been started by another process. If the parent
    process is not alive then the server should exit(see exit notification)
    its process.
    '''
    processId:  Optional[int]

    '''
    The capabilities provided by the client(editor or tool)
    '''
    capabilities: ClientCapabilities


class InitializedParams(TypedDict):
    '''
    https://microsoft.github.io/language-server-protocol/specifications/specification-current/#initialized
    '''


class DidOpenTextDocumentParams(TypedDict):
    '''
    The document that was opened.
    '''
    textDocument: TextDocumentItem
