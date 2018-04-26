var Proxy = artifacts.require("Proxy");
var TokenVersion1 = artifacts.require("TokenVersion1");
var TokenVersion2 = artifacts.require("TokenVersion2");

module.exports = function(deployer) {
  deployer.deploy(Proxy);
  deployer.deploy(TokenVersion1);
  deployer.deploy(TokenVersion2);
};
