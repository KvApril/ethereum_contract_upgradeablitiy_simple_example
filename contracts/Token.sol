pragma solidity ^0.4.21;

contract TokenVersion1 {
    mapping (address => uint) balances;

    event Transfer(address _from, address _to, uint256 _value);

    function balanceOf(address addr) public view returns (uint) {
        return balances[addr];
    }

    function transfer(address to, uint256 value) public {
        require(balances[msg.sender] >= value);
        balances[msg.sender] -= value;
        balances[to] += value;
        emit Transfer(msg.sender, to, value);
    }

    // there is a bug in this function: value should not
    // be multiplied by 2
    function mint(address to, uint256 value) public {
        balances[to] += value * 2;
        emit Transfer(0x0, to, value);
    }
}

contract TokenVersion2 is TokenVersion1 {

    // bug corrected here: multiplication by 2 removed
    function mint(address to, uint256 value) public {
        balances[to] += value;
        emit Transfer(0x0, to, value);
    }
}