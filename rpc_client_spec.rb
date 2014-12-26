require_relative 'rpc_client'

describe RpcClient do

  it 'should calculate the fibonacci for a number' do
    expect(RpcClient.execute(method: 'fib', params: { number: '30' })).to eq('')
  end

  after do
    RpcClient.channel.close
    RpcClient.connection.close
  end
end
