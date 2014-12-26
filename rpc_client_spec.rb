require_relative 'rpc_client'

describe RpcClient do

  it 'should calculate the fibonacci for a number' do
    expect(RpcClient.execute(30)).to eq(832040)
  end

  after do
    RpcClient.channel.close
    RpcClient.connection.close
  end
end
