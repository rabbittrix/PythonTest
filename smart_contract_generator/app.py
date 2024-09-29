import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from flask import Response

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        dbc.NavbarSimple(
            brand="Smart Contract Generator with Solidity",
            brand_href="#",
            color="primary",
            dark=True,
            className="navbar"
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Nav(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(dbc.Label("Select Contract Type"), width=4),
                                    dbc.Col(
                                        dcc.Dropdown(
                                            id="contract-type",
                                            options=[
                                                {"label": "ERC20", "value": "erc20"},
                                                {"label": "ERC721", "value": "erc721"},
                                                {"label": "ERC1155", "value": "erc1155"},
                                                {"label": "Governor", "value": "governor"},
                                            ],
                                            value="erc20",
                                        ),
                                        width=8
                                    ),
                                ],
                                className="mb-3"
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(dbc.Label("Token Name"), width=4),
                                    dbc.Col(dbc.Input(id="token-name", placeholder="Enter token name"), width=8),
                                ],
                                className="mb-3"
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(dbc.Label("Token Symbol"), width=4),
                                    dbc.Col(dbc.Input(id="token-symbol", placeholder="Enter token symbol"), width=8),
                                ],
                                className="mb-3"
                            ),
                            dbc.Button("Generate", id="generate-button", color="primary", className="mt-2"),
                        ],
                        vertical=True,
                        pills=True,
                        className="sidebar",
                    ),
                    width=3,
                ),
                dbc.Col(
                    [
                        html.H2("Generated Smart Contract"),
                        html.Pre(id="contract-output", style={"whiteSpace": "pre-wrap"}),
                        dbc.Button("Download", id="download-button", color="primary", className="mt-2", href="/download/smartcontract.sol"),
                    ],
                    width=9,
                ),
            ],
        ),
    ],
    fluid=True,
)

@app.callback(
    Output("contract-output", "children"),
    Input("generate-button", "n_clicks"),
    [
        Input("contract-type", "value"),
        Input("token-name", "value"),
        Input("token-symbol", "value"),
    ],
)
def generate_contract(n_clicks, contract_type, token_name, token_symbol):
    if n_clicks is None:
        return ""

    if contract_type == "erc20":
        contract = f"""
        // SPDX-License-Identifier: MIT
        pragma solidity ^0.8.20;

        import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
        import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Permit.sol";

        contract {token_name} is ERC20, ERC20Permit {{
            constructor() ERC20("{token_name}", "{token_symbol}") ERC20Permit("{token_name}") {{}}
        }}
        """
    elif contract_type == "erc721":
        contract = f"""
        // SPDX-License-Identifier: MIT
        pragma solidity ^0.8.20;

        import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

        contract {token_name} is ERC721 {{
            constructor() ERC721("{token_name}", "{token_symbol}") {{}}
        }}
        """
    elif contract_type == "erc1155":
        contract = f"""
        // SPDX-License-Identifier: MIT
        pragma solidity ^0.8.20;

        import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
        import "@openzeppelin/contracts/access/Ownable.sol";

        contract {token_name} is ERC1155, Ownable {{
            constructor(address initialOwner) ERC1155("") Ownable(initialOwner) {{}}

            function setURI(string memory newuri) public onlyOwner {{
                _setURI(newuri);
            }}
        }}
        """
    elif contract_type == "governor":
        contract = f"""
        // SPDX-License-Identifier: MIT
        pragma solidity ^0.8.20;

        import "@openzeppelin/contracts/governance/Governor.sol";
        import "@openzeppelin/contracts/governance/extensions/GovernorSettings.sol";
        import "@openzeppelin/contracts/governance/extensions/GovernorCountingSimple.sol";
        import "@openzeppelin/contracts/governance/extensions/GovernorVotes.sol";
        import "@openzeppelin/contracts/governance/extensions/GovernorVotesQuorumFraction.sol";
        import "@openzeppelin/contracts/governance/extensions/GovernorTimelockControl.sol";

        contract {token_name} is Governor, GovernorSettings, GovernorCountingSimple, GovernorVotes, GovernorVotesQuorumFraction, GovernorTimelockControl {{
            constructor(IVotes _token, TimelockController _timelock)
                Governor("{token_name}")
                GovernorSettings(7200 /* 1 day */, 50400 /* 1 week */, 0)
                GovernorVotes(_token)
                GovernorVotesQuorumFraction(4)
                GovernorTimelockControl(_timelock)
            {{}}

            // The following functions are overrides required by Solidity.

            function votingDelay()
                public
                view
                override(Governor, GovernorSettings)
                returns (uint256)
            {{
                return super.votingDelay();
            }}

            function votingPeriod()
                public
                view
                override(Governor, GovernorSettings)
                returns (uint256)
            {{
                return super.votingPeriod();
            }}

            function quorum(uint256 blockNumber)
                public
                view
                override(Governor, GovernorVotesQuorumFraction)
                returns (uint256)
            {{
                return super.quorum(blockNumber);
            }}

            function state(uint256 proposalId)
                public
                view
                override(Governor, GovernorTimelockControl)
                returns (ProposalState)
            {{
                return super.state(proposalId);
            }}

            function proposalNeedsQueuing(uint256 proposalId)
                public
                view
                override(Governor, GovernorTimelockControl)
                returns (bool)
            {{
                return super.proposalNeedsQueuing(proposalId);
            }}

            function proposalThreshold()
                public
                view
                override(Governor, GovernorSettings)
                returns (uint256)
            {{
                return super.proposalThreshold();
            }}

            function _queueOperations(uint256 proposalId, address[] memory targets, uint256[] memory values, bytes[] memory calldatas, bytes32 descriptionHash)
                internal
                override(Governor, GovernorTimelockControl)
                returns (uint48)
            {{
                return super._queueOperations(proposalId, targets, values, calldatas, descriptionHash);
            }}

            function _executeOperations(uint256 proposalId, address[] memory targets, uint256[] memory values, bytes[] memory calldatas, bytes32 descriptionHash)
                internal
                override(Governor, GovernorTimelockControl)
            {{
                super._executeOperations(proposalId, targets, values, calldatas, descriptionHash);
            }}

            function _cancel(address[] memory targets, uint256[] memory values, bytes[] memory calldatas, bytes32 descriptionHash)
                internal
                override(Governor, GovernorTimelockControl)
                returns (uint256)
            {{
                return super._cancel(targets, values, calldatas, descriptionHash);
            }}

            function _executor()
                internal
                view
                override(Governor, GovernorTimelockControl)
                returns (address)
            {{
                return super._executor();
            }}
        }}
        """

    global contract_output
    contract_output = contract

    return contract

@app.server.route("/download/smartcontract.sol")
def download_contract():
    return Response(
        contract_output,  # Use the generated contract content
        mimetype="text/plain",
        headers={"Content-disposition": "attachment; filename=smartcontract.sol"}
    )

if __name__ == "__main__":
    app.run_server(debug=True)
