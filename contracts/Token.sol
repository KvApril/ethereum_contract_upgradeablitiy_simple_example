pragma solidity ^0.4.21;

contract TokenVersion1 {
    mapping (address => uint) balances;

    event Transfer(address _from, address _to, uint256 _value);

    function balanceOf(address _address) public view returns (uint) {
        return balances[_address];
    }

    function transfer(address _to, uint256 _value) public {
        require(balances[msg.sender] >= _value);
        balances[msg.sender] -= _value;
        balances[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
    }

    // there is a bug in this function: value should not
    // be multiplied by 2
    function mint(address _to, uint256 _value) public {
        balances[_to] += _value * 2;
        emit Transfer(0x0, _to, _value);
    }
}

contract TokenVersion2 is TokenVersion1 {

    // bug corrected here: multiplication by 2 removed
    function mint(address _to, uint256 _value) public {
        balances[_to] += _value;
        emit Transfer(0x0, _to, _value);
    }
}