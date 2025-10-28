// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract IdentityNFT is ERC721, AccessControl {
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant CANCELER_ROLE = keccak256("CANCELER_ROLE");
    struct NFTData { bool active; uint256 createdAt; uint256 canceledAt; uint256 previousId; string tokenURIData; }
    mapping(address => uint256) public activeNFT;
    mapping(uint256 => NFTData) public nftHistory;
    uint256 private _nextId;
    event MintingEvent(uint256 indexed tokenId, address indexed user);
    event CancelamentoEvent(uint256 indexed oldTokenId, uint256 indexed newTokenId);
    event CancelamentoSimples(uint256 indexed tokenId);

    constructor(address admin) ERC721("Blocktrust Identity","BID"){
        _grantRole(DEFAULT_ADMIN_ROLE,admin);
        _grantRole(MINTER_ROLE,admin);
        _grantRole(CANCELER_ROLE,admin);
        _nextId=1;
    }

    function mintIdentityNFT(address user,string memory tokenURIData,uint256 previousId) external onlyRole(MINTER_ROLE) returns(uint256){
        uint256 current=activeNFT[user];
        if(current!=0 && nftHistory[current].active){
            nftHistory[current].active=false;
            nftHistory[current].canceledAt=block.timestamp;
            emit CancelamentoEvent(current,_nextId);
        }
        uint256 tokenId=_nextId++;
        _safeMint(user,tokenId);
        activeNFT[user]=tokenId;
        nftHistory[tokenId]=NFTData(true,block.timestamp,0,previousId,tokenURIData);
        emit MintingEvent(tokenId,user);
        return tokenId;
    }

    function cancelNFT(uint256 tokenId) external onlyRole(CANCELER_ROLE){
        require(_exists(tokenId),"NFT inexistente");
        require(nftHistory[tokenId].active,"Ja cancelado");
        nftHistory[tokenId].active=false;
        nftHistory[tokenId].canceledAt=block.timestamp;
        emit CancelamentoSimples(tokenId);
    }

    function isActive(uint256 tokenId) external view returns(bool){
        return _exists(tokenId)&&nftHistory[tokenId].active;
    }

    function tokenURI(uint256 tokenId) public view override returns(string memory){
        require(_exists(tokenId),"Token inexistente");
        return nftHistory[tokenId].tokenURIData;
    }

    function _update(address to,uint256 tokenId,address auth) internal override returns(address){
        address from=_ownerOf(tokenId);
        if(from!=address(0)&&to!=address(0)) revert("SBT: transfer proibido");
        return super._update(to,tokenId,auth);
    }

    function supportsInterface(bytes4 interfaceId) public view override(ERC721, AccessControl) returns (bool) {
        return super.supportsInterface(interfaceId);
    }
}
