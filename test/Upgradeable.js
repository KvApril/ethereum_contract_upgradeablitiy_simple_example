// 1. delete build folder
// 2. restart ganache
// 3. run this test: truffle test

const TokenVersion1 = artifacts.require('TokenVersion1')
const TokenVersion2 = artifacts.require('TokenVersion2')
const Proxy = artifacts.require('Proxy')

contract('Upgradeable', function (accounts) {
    var sender = accounts[1]
    var receiver = accounts[2]

    it('should work', async function () {
        const impl_v1 = await TokenVersion1.new()
        const impl_v2 = await TokenVersion2.new()
        const impl_proxy = await Proxy.new()

        await impl_proxy.upgradeTo(impl_v1.address)

        await TokenVersion1.at(impl_proxy.address).mint(sender, 100)

        const balance1 = await TokenVersion1.at(impl_proxy.address).balanceOf(sender)
        console.log("balance first mint ", balance1.toNumber())    

        await impl_proxy.upgradeTo(impl_v2.address)
        
        await TokenVersion2.at(impl_proxy.address).mint(sender, 100)

        const balance2 = await TokenVersion2.at(impl_proxy.address).balanceOf(sender)
        console.log("balance 2nd mint ", balance2.toNumber())

        const transferTx = await TokenVersion2.at(impl_proxy.address).transfer(receiver, 10, { from: sender })

        console.log("Transfer TX gas cost using Inherited Storage Proxy", transferTx.receipt.gasUsed)

        const balance = await TokenVersion2.at(impl_proxy.address).balanceOf(sender)
        assert(balance.eq(290))
    })

})
