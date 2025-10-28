// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
interface IIdentityNFT{function isActive(uint256 tokenId) external view returns(bool);function activeNFT(address user) external view returns(uint256);}
contract ProofRegistry{
    struct Proof{string docHash;address signer;string proofUrl;uint256 timestamp;bool revoked;}
    mapping(string=>Proof) public proofs;
    IIdentityNFT public identity;
    event ProofRegistered(string indexed docHash,address indexed signer,uint256 timestamp);
    event ProofRevoked(string indexed docHash,address indexed by,uint256 timestamp);
    constructor(address identityContract){identity=IIdentityNFT(identityContract);}
    function registerProof(string calldata docHash,string calldata proofUrl) external{
        uint256 tokenId=identity.activeNFT(msg.sender);
        require(tokenId!=0&&identity.isActive(tokenId),"Identidade inativa");
        proofs[docHash]=Proof(docHash,msg.sender,proofUrl,block.timestamp,false);
        emit ProofRegistered(docHash,msg.sender,block.timestamp);
    }
    function verifyProof(string calldata docHash) external view returns(Proof memory){return proofs[docHash];}
    function revokeProof(string calldata docHash) external{
        Proof storage p=proofs[docHash];
        require(p.signer==msg.sender,"Somente o signatario pode revogar");
        p.revoked=true;
        emit ProofRevoked(docHash,msg.sender,block.timestamp);
    }
}
